# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cevote.voting.models import Candidate, Position
from cevote.voting.forms import PositionForm, CandidateForm, \
                                create_position_forms_list

def vote(request):
    if request.method == "POST":
        pforms = {}
        for pos in Position.objects.all():
#            pform = PositionForm(request.POST, instance=pos, \
#                    prefix="pos_%s" % pos, instance = pos.get())
            cforms = [CandidateForm(request.POST, prefix="cand_%s" % cand, \
                    instance=cand) for cand in pos.candidate_set.all()]
            pforms[pos] = cforms
        # We've just created a dictionary of {PositionForm:[CandidateForm1, CandidateForm2, ...], ...}
#        for pform, cforms in pforms.items():
            #if pform.is_valid() and all([cf.is_valid() for cf in cforms]):
    else:
        pforms = {}
        for pos in Position.objects.all():
            #pform = PositionForm(instance=pos, prefix="pos_%s" % pos)
            cforms = [CandidateForm(prefix="cand_%s" % cand, \
                    instance=cand) for cand in pos.candidate_set.all()]
            pforms[pos] = cforms
        # We've just created a dictionary of {PositionForm:[CandidateForm1, CandidateForm2, ...], ...}
        return render_to_response('vote.html', {'position_forms': pforms}) 

def thanks(request):
    return HttpResponse(_("Your vote has been successfully submitted."))
