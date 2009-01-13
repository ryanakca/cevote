#
# Admin Forms for the voting application
# Copyright (C) 2009  Ryan Kavanagh <ryanakca@kubuntu.org>
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
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from vote.models import Voter

class CreateVoterForm(forms.ModelForm):
    """
    Form to create voters under the admin interface. It collects the number
    of voters the administrator wishes to creates.
    """
    number = forms.IntegerField(label=_("Number of voters"))

    class Meta:
        model = Voter
        exclude = ('user', 'has_voted')
