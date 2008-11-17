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
        raise str(request.POST)
        for pos in Position.objects.all():
            pforms.append(PositionForm(pos, request.POST))
        for form in pforms:
            if form.is_valid():
                raise request.data
#                selected_candidate = form.pos.candidate_set.get(id = form[candidates])
#                selected_candidate.votes += 1
#                selected_candidate.save()
            else:
                pass
        HttpResponse(_("Your vote has been successfully submitted."))
    else:
        pforms = [] 
        for pos in Position.objects.all():
            pforms.append(PositionForm(pos, prefix="pos_%d" % pos.id))
        return render_to_response('vote.html', {'position_forms': pforms}) 
