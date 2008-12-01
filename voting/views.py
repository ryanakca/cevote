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

# *Sigh*, why must I import Position as PositionModel?
# If I don't, I get the following exception:
# local variable 'Position' referenced before assignment
from cevote.voting.models import Position as PositionModel
from cevote.voting.forms import PositionForm as My_PositionForm

def vote(request):
    # We must specify the fields since there's a bug in Drupal that causes
    # modelformset_factory to ignore the Meta class in forms
    PositionFormset = modelformset_factory(PositionModel,
            form=My_PositionForm, fields=('candidate_set'))
    if request.method == "POST":
        formset = PositionFormset(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for Position in instances:
                for candidate in Position.cleaned_data:
                    candidate.votes += 1
                    candidate.save()
            HttpResponse(_("Your vote has been successfully submitted."))
    else:
        forms = PositionFormset()
        return render_to_response('vote.html', {'position_forms':forms})
