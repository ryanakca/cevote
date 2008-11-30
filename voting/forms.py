from django import forms
from models import Position, Candidate
from django.utils.translation import ugettext_lazy as _

class PositionForm(forms.ModelForm):
    candidate_set = forms.ModelMultipleChoiceField(
            Candidate.objects.all(),
            widget = forms.CheckboxSelectMultiple())

    class Meta:
        model = Position
        fields = ('candidate_set')

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['candidate_set'].queryset = self.instance.candidate_set.all()
        self.name = self.instance.name
        self.weight = self.instance.weight
        self.number = self.instance.amount_of_electees

    def clean(self):
        candidates = self.cleaned_data.get('candidate_set')
        if len(self.fields['candidates'].queryset) == \
                (self.number - 1):
            return cleaned_data
        else:
            raise forms.ValidationError(_("Selected too many candidates. "
                "Select %d instead" % self.amount_of_electees))
