# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cevote.voting.models import Candidate, Position
from cevote.voting.forms import PositionForm, create_position_forms_list

def vote(request):
    """ Used during the vote, displays positions and candidates. """
    if request.method == 'POST':
        # Submitting information here
        form_list = create_position_forms_list(request.POST)
        for form in form_list:
            if not form.is_valid():
                break
            for cand in form.cadidate_set:
                cand.votes += 1
        else:
            # Prevent hitting back to resubmit
            return HttpResponseRedirect(reverse('thanks'))
    else:
        # Displaying vote form
        form_list = []
        for pos in Position.objects.all():
            form_list.append(PositionForm(pos, prefix="pos_%s" % pos, instance=pos)) 
    return render_to_response('vote.html', {'forms': form_list})


def thanks(request):
    return HttpResponse(_("Your vote has been successfully submitted."))
