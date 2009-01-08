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

from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.template import RequestContext

from vote.models import Position, Voter, Group
from vote.admin_forms import CreateVoterForm

def results(request):
    candidate_position_dict = {}
    for pos in Position.objects.all():
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
    return render_to_response('admin/vote/results.html', \
        {'candidate_position_dict': candidate_position_dict})

def create_voters(request):
    if request.method == 'POST': 
        form = CreateVoterForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            group = form.cleaned_data['group']
            voter_number = User.objects.all().count() + 1
            for i in range(number):
                # We must make sure that there isn't already a user with the
                # username "voter_%d" % i.
                while User.objects.filter(username="voter_%d" % 
                    (voter_number + i)):
                    voter_number += 1
                u = User(username="voter_%d" % (voter_number + i), 
                         password='')
                u.save()
                u.set_unusable_password()
                v = Voter(user=u, group=group)
                v.save()
            request.user.message_set.create(message=_("Created %d voters in"\
            " group %s." % (number, group)))
            #"%s group" % (number, group)))
            return render_to_response('admin/vote/add_voters.html',
                {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('admin/vote/add_voters.html', \
                {'form': form})
    else:
        form = CreateVoterForm()
        return render_to_response('admin/vote/add_voters.html', \
           {'form': form})
