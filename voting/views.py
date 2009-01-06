# Views for the voting application.
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

import os

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as django_login

# *Sigh*, why must I import Position as PositionModel?
# If I don't, I get the following exception:
# local variable 'Position' referenced before assignment
from cevote.voting.models import Position as PositionModel
from cevote.voting.forms import PositionForm as My_PositionForm
from cevote.settings import PRINT

@user_passes_test(lambda u: u.is_authenticated(), login_url='/vote/login.html')
def vote(request):
    # We must specify the fields since there's a bug in Drupal that causes
    # modelformset_factory to ignore the Meta class in forms
    PositionFormset = modelformset_factory(PositionModel,
            form=My_PositionForm, fields=('candidate_set'))
    if request.method == "POST":
        formset = PositionFormset(data=request.POST)
        if formset.is_valid():
            print_list = []
            for Position in formset.cleaned_data:
                if Position.has_key('candidate_set'):
                    for candidate in Position['candidate_set']:
                        candidate.votes += 1
                        candidate.save()
                    print_list.append(str((PositionModel.objects.get(id= \
                        Position['id']),
                        Position['candidate_set'])))
            if PRINT['PRINT_VOTES']:
                print_data = '\n'.join(print_list)
                fd = os.popen("lp -d %s" % PRINT['PRINTER'], "wb")
                fd.write(print_data)
            return HttpResponseRedirect('/success/')
        else:
            return render_to_response('vote.html', {'position_forms':formset})
    else:
        forms = PositionFormset()
        return render_to_response('vote.html', {'position_forms':forms})

def login(request):
    if request.POST.has_key('uuid'):
        uuid = request.POST['uuid']
        user = authenticate(uuid=uuid)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return HttpResponseRedirect('/vote/')
            else:
                return render_to_response('vote/login.html',
                        {'uuid': uuid,
                         'error_msg': _("UUID Disabled.")})
        else:
            return render_to_response('vote/login.html',
                    {'uuid': uuid,
                     'error_msg': _("Invalid UUID or UUID has already voted")})
    else:
        return render_to_response('vote/login.html')
