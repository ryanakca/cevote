from django import forms
from models import Position, Candidate

class PositionForm(forms.ModelForm):

    def __init__(self, position, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['candidates'].widget = forms.SelectMultiple()
        self.fields['candidates'].queryset = position.candidate_set.\
            order_by('initial').order_by('first_name').order_by('last_name')
        self.position = position.name


def create_position_forms_list(data=None):
    positions = Position.objects.all().order_by('weight')
    form_list = []
    for pos in positions:
        form_list.append(PositionForm(pos, data, prefix="pos_%s" % pos))
    return form_list
