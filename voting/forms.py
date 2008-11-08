from django import forms
from models import Position, Candidate

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
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        exclude = ['weight', 'amount_of_electees', 'voting_groups']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        exclude = ['position']

def create_position_forms_list(data=None):
    positions = Position.objects.all().order_by('weight')
    form_list = []
    for pos in positions:
        form_list.append(PositionForm(pos, prefix="pos_%s" % pos, instance=pos))
    return form_list
