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
import datetime

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, logout, login as django_login
from django.contrib.auth.models import User
from django.template import RequestContext

# *Sigh*, why must I import Position as PositionModel?
# If I don't, I get the following exception:
# local variable 'Position' referenced before assignment
from vote.models import ElectionDateTime, Position as PositionModel
from vote.forms import PositionForm as My_PositionForm
from vote.settings import PRINT

@user_passes_test(lambda u: u.is_authenticated(), login_url='/vote/login/')
def vote(request):
    """
    Voting ballot view.

    @type request: HttpRequest
    @rtype: HttpResponse
    """
    # Getting the user data from profile
    group = request.user.get_profile().group
    positions = \
        PositionModel.objects.filter(voting_groups=group).order_by('weight')
    # We must specify the fields since there's a bug in Drupal that causes
    # modelformset_factory to ignore the Meta class in forms
    PositionFormset = modelformset_factory(PositionModel,
            form=My_PositionForm, fields=('candidate_set'))
    if request.method == "POST" and \
            not request.user.get_profile().has_voted:
        formset = PositionFormset(data=request.POST, queryset=positions)
        if formset.is_valid():
            vote_percentage = request.user.get_profile().group.vote_percentage
            if request.POST.has_key('confirmed'):
                print_list = [_("Vote percentage: %d") % vote_percentage]
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
                request.user.message_set.create(
                message=ugettext("Please verify your choices since all votes are"+\
                " final."))
                return render_to_response('vote/vote.html',
                       {'position_forms': formset,
                        'confirmed': 'confirmed'},
                       context_instance=RequestContext(request))
        else:
            return render_to_response('vote/vote.html', 
            {'position_forms':formset})
    else:
        forms = PositionFormset(queryset=positions)
        return render_to_response('vote/vote.html', {'position_forms':forms})

def login(request):
    """
    UUID login view.

    @type request: HttpRequest
    @rtype: HttpResponse
    """

    def _render_error(uuid, message):
        """
        @type uuid: str
        @param uuid: UUID
        @type message: str
        @param message: error message
        @rtype: HttpResponse
        @return: UUID login form with UUID and error message.
        """
        return render_to_response('vote/login.html', {'uuid': uuid,
                 'error_msg': _(message)})

    if len(ElectionDateTime.objects.filter(start__lt=\
        datetime.datetime.now()).filter(end__gt=datetime.datetime.now())) == 0:
        return _render_error('', 'It is not yet time to vote')

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
