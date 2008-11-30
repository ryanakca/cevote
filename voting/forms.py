from django import forms
from models import Position, Candidate
from django.utils.translation import ugettext_lazy as _

class PositionForm(forms.Form):
    candidates = forms.ModelMultipleChoiceField(widget = \
        forms.CheckboxSelectMultiple(), queryset = Candidate.objects.all())

    def __init__(self, candidates, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['candidates'].queryset = candidates
        self.weight = self.fields['candidates'].queryset[0].position.weight
        self.name = self.fields['candidates'].queryset[0].position.name
        self.number = self.fields['candidates'].queryset[0].position.amount_of_electees

    def clean(self):
        cleaned_data = self.cleaned_data
        candidates = cleaned_data.get('candidates')
        if len(self.fields['candidates'].queryset) == (self.number - 1):
            return cleaned_data
        else:
            raise forms.ValidationError(_("Selected too many candidates. "
                "Select %d instead" % self.number))
