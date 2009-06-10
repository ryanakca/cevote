#
# Forms for the voting application
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
from django import forms
from django.utils.translation import ugettext_lazy as _
from cevote.vote.models import Position, Candidate
from cevote.vote.SelectCandidateWidget import SelectCandidateWidget

class PositionForm(forms.ModelForm):
    """ Position form vor the voting page. """
    candidate_set = forms.ModelMultipleChoiceField(
            Candidate.objects.all(),
            widget = SelectCandidateWidget)

    def __init__(self, *args, **kwargs):
        """
        Initializes the form. Sets form's candidate_set to the positions, and
        the form's name, weight and number of electees to their appropriate
        values.
        """
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['candidate_set'].queryset =\
                                self.instance.candidate_set.all()
        self.name = self.instance.name
        self.weight = self.instance.weight
        self.number = self.instance.amount_of_electees

    def clean(self):
        """
        Ensures that the user supplied data is clean.

        @raise forms.ValidationError: If the wrong number of candidates is
            selected
        @return: cleaned_data
        """

        if self.cleaned_data.has_key('candidate_set') and \
            (len(self.cleaned_data['candidate_set']) == self.number):
            return self.cleaned_data
        else:
            raise forms.ValidationError(_("Selected wrong number of "
                "candidates. Select %d instead." % self.number))

    class Meta:
        """
        ModelForm Meta class. Sets the ModelForm's model and the fields to
        exclude.
        """
        model = Position
        # fields = ('candidate_set')
        exclude = ('amount_of_electees', 'name', 'weight')
