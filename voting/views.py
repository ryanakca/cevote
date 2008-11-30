# Views for the voting application.
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
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory

from cevote.voting.models import Candidate, Position
from cevote.voting.forms import PositionForm

def vote(request):
    if request.method == "POST":
        PositonFormset = modelformset_factory(Position, form=PositionForm)
#        pforms = []
#        for pos in Position.objects.all():
#            pforms.append(PositionForm(request.POST, prefix="pos_%d" % pos.id))
#        for form in pforms:
#            if form.is_valid():
#                for candidate in form.cleaned_data:
#                    selected_candidate = Candidates.object.get(id = \
#                    int(candidate))
#                    selected_candidate.votes += 1
#                    selected_candidate.save()
#            else:
#                HttpResponse(_("Your vote has been successfully submitted."))
    else:
        PositionFormset = modelformset_factory(Position, form=PositionForm)
        
#        pforms = [] 
#        for pos in Position.objects.all():
#            pforms.append(PositionForm(pos.candidate_set.order_by('inital').\
#                order_by('first_name').order_by('last_name').all(), \
#                prefix="pos_%d" % pos.id))
#        return render_to_response('vote.html', {'position_forms': pforms}) 
