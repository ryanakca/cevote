from django import forms
from models import Position, Candidate
from django.utils.translation import ugettext_lazy as _

#class PositionForm(forms.ModelForm):
#    def __init__(self, position, *args, **kwargs):
#        super(PositionForm, self).__init__(*args, **kwargs)
#        self.fields['candidate_set'].widget = forms.SelectMultiple()
#        self.fields['candidate_set'].queryset = position.candidate_set.\
#            order_by('initial').order_by('first_name').order_by('last_name').all()
#        self.position = position.name
#
#    class Meta:
#        model = Position

# http://www.42topics.com/dumps/django/docs.html 
#class PositionForm(forms.Form):
#    name = forms.Charfield()
#    candidates = forms.ModelMultipleChoiceField(widget = \
#        forms.SelectMultiple(), queryset = Candidates.objects.all()
#
#    def __init__(self, position, *args, **kwargs):
#        self.name = position.name
#        self.candidates = position.candidate_set.all()
#        super(PositionForm, self).__init__(*args, **kwargs)
# http://collingrady.wordpress.com/2008/02/18/editing-multiple-objects-in-django-with-newforms/ 

class PositionForm(forms.Form):
    candidates = forms.ModelMultipleChoiceField(widget = \
        forms.CheckboxSelectMultiple(), queryset = Candidate.objects.all())

    def __init__(self, position, *args, **kwargs):
        self.name = position.name
        self.weight = position.weight
        self.number = position.amount_of_electees
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['candidates'].queryset = position.candidate_set.order_by('initial').order_by('first_name').order_by('last_name').all()

    def clean(self):
        cleaned_data = self.cleaned_data
        candidates = cleaned_data.get('candidates')
        if len(self.fields['candidates'].queryset) == (self.number - 1):
            return cleaned_data
        else:
            raise forms.ValidationError(_("Selected too many candidates. "
                "Select %d instead" % self.number))

def create_position_forms_list(data=None):
    positions = Position.objects.all().order_by('weight')
    form_list = []
    for pos in positions:
        form_list.append(PositionForm(pos, prefix="pos_%s" % pos, instance=pos))
    return form_list
