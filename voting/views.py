# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cevote.voting.models import Candidate, Position
from cevote.voting.forms import PositionForm

def vote(request):
    if request.method == "POST":
        pforms = []
        for pos in Position.objects.all():
            pforms.append(PositionForm(pos, request.POST, prefix="pos_%d" % pos.id))
        for form in pforms:
            if form.is_valid() == False:
                raise str(form.changed_data)
                for candidate in form.cleaned_data:
                    selected_candidate = Candidates.object.get(id = \
                    int(candidate))
                    selected_candidate.votes += 1
                    selected_candidate.save()
            else:
                HttpResponse(_("Your vote has been successfully submitted."))
    else:
        pforms = [] 
        for pos in Position.objects.all():
            pforms.append(PositionForm(pos, prefix="pos_%d" % pos.id))
        return render_to_response('vote.html', {'position_forms': pforms}) 
