# View for the results
# Copyright (C) 2008  Ryan Kavanagh <ryanakca@kubuntu.org>
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
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from cevote.voting.models import Position

@login_required
@permission_required(lambda u: u.is_staff())
def index(request):
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
    return render_to_response('results/index.html', \
        {'candidate_position_dict': candidate_position_dict})
