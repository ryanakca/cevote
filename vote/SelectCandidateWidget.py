#
# Widgets for the voting application's form
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
# The SelectCandidateWidget is a derivative of Django's CheckboxSelectMultiple.
# The original work was licensed under the following license:
##  
## Copyright (c) Django Software Foundation and individual contributors.
## All rights reserved.
## 
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
## 
##     1. Redistributions of source code must retain the above copyright notice,
##        this list of conditions and the following disclaimer.
## 
##     2. Redistributions in binary form must reproduce the above copyright
##        notice, this list of conditions and the following disclaimer in the
##        documentation and/or other materials provided with the distribution.
## 
##     3. Neither the name of Django nor the names of its contributors may be
##        used to endorse or promote products derived from this software
##        without specific prior written permission.
## 
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
## POSSIBILITY OF SUCH DAMAGE. 
## 

from django import forms
from django.forms.widgets import CheckboxInput
from django.forms.fields import Field
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from itertools import chain

class SelectCandidateWidget(forms.CheckboxSelectMultiple):
    """ 
    A widget that allows voters to select a candidate. It display's the
    Candidate's name and picture side by side in a <p>
    """
    
    def render(self, name, value, attrs=None, choices=()):
        """
        Renders the widget.

        @rtype: unicode
        @return: html tablerows (<tr>) each containing a checkbox with the
        candidate's name and picture beside it.
        """
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = []
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''
            # Does the candidate have a picture?
            if self.choices.queryset.get(pk=option_value).picture:
                pictureurl = unicode(self.choices.queryset.get(pk=option_value).picture.url)
            else:
                pictureurl = ''
            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<tr>'\
                                '<td><label%s>%s %s</label></td>'\
                                '<td><img src="%s" class="candidate_picture" /></td>'\
                           '</tr>' % \
                           (label_for, rendered_cb, option_label, pictureurl))
        return mark_safe(u'\n'.join(output))

