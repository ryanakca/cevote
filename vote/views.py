# Views for the voting application.
# Copyright (C) 2008, 2009  Ryan Kavanagh <ryanakca@kubuntu.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, user_passes_test, \
                        permission_required
from django.contrib.auth import authenticate, logout, login as django_login
from django.contrib.auth.models import User

# *Sigh*, why must I import Position as PositionModel?
# If I don't, I get the following exception:
# local variable 'Position' referenced before assignment
from vote.models import Position as PositionModel
from vote.forms import PositionForm as My_PositionForm
from cevote.settings import PRINT

@user_passes_test(lambda u: u.is_authenticated(), login_url='/vote/login/')
def vote(request):
    # Getting the user data from profile
    group = request.user.get_profile().group
    positions = \
        PositionModel.objects.filter(voting_groups=group).order_by('weight')
    # We must specify the fields since there's a bug in Drupal that causes
    # modelformset_factory to ignore the Meta class in forms
    PositionFormset = modelformset_factory(PositionModel,
            form=My_PositionForm, fields=('candidate_set'))
    if request.method == "POST":
        vote_percentage = request.user.get_profile().group.vote_percentage
        formset = PositionFormset(data=request.POST, queryset=positions)
        if formset.is_valid():
            print_list = []
            for Position in formset.cleaned_data:
                if Position.has_key('candidate_set'):
                    for candidate in Position['candidate_set']:
                        # We must devide the vote_percentage by 100 since it's
                        # an integer between 0 and 100, and we want to cast a
                        # percent of a vote (half a vote, a whole vote, etc)
                        candidate.votes += 1 * (vote_percentage / 100)
                        candidate.save()
                    print_list.append(str((PositionModel.objects.get(id= \
                        Position['id']),
                        Position['candidate_set'])))
            if PRINT['PRINT_VOTES']:
                print_data = '\n'.join(print_list)
                fd = os.popen("lp -d %s" % PRINT['PRINTER'], "wb")
                fd.write(print_data)
            # Set the UUID as used.
            request.user.get_profile().has_voted = True
            request.user.get_profile().save()
            return HttpResponseRedirect('/vote/success/')
        else:
            return render_to_response('vote.html', {'position_forms':formset})
    else:
        forms = PositionFormset(queryset=positions)
        return render_to_response('vote.html', {'position_forms':forms})

def login(request):
    def _render_error(uuid, message):
        return render_to_response('vote/login.html', {'uuid': uuid,
                 'error_msg': _(message)})

    if request.POST.has_key('uuid'):
        uuid = request.POST['uuid']
        try:
            user = authenticate(uuid=uuid)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect('/vote/')
                else:
                    return _render_error(uuid, "UUID Disabled.")
            else:
                return _render_error(uuid,
                        "Invalid UUID or UUID has already voted.")
        except User.DoesNotExist:
            return _render_error(uuid,
                        "Invalid UUID or UUID has already voted.")
    else:
        return render_to_response('vote/login.html')

@login_required
@permission_required(lambda u: u.is_staff())
def results(request):
    candidate_position_dict = {}
    for pos in PositionModel.objects.all():
        # Create a dictionary of positions : [ [candidate1, wins?], [candidate2,
        # wins?], ...]
        candidate_position_dict[pos] = []
        for can in pos.candidate_set.all().order_by('-votes'):
            candidate_position_dict[pos].append([can, False])
    for p in candidate_position_dict.keys():
        if candidate_position_dict[p] == []:
            # There aren't any candidates or nobody can win, let's remove
            # the position from the dictionary
            del candidate_position_dict[p]
        else:
        # Set the winners win value to True
            # Use min, because there might be less candidates than the required
            # amount
            for winner in range(min(p.amount_of_electees, \
                                len(candidate_position_dict[p]))):
                candidate_position_dict[p][winner][1] = True
            # If there are ties, set them to True too
            last_tie = p.amount_of_electees
            while (last_tie < len(candidate_position_dict[p])) and \
                  (candidate_position_dict[p][last_tie][0].votes \
                    == candidate_position_dict[p][last_tie - 1][0].votes):
                candidate_position_dict[p][last_tie][1] = True
                last_tie += 1
    return render_to_response('vote/results.html', \
        {'candidate_position_dict': candidate_position_dict})
