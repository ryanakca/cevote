# copyright template tag
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

from django import template

register = template.Library()

@register.simple_tag
def copyright(commaseperatedyears):
    """ Template tag that prints a copyright notice. """
    years = commaseperatedyears.split(',')
    for i in years:
        if not i.isalnum():
            raise template.TemplateSyntaxError,  "Expected input is comma" + \
                  " seperated years (example: 2000,2001). Received %r" % \
                  commaseperatedyears

    copyright_msg = [
u'Copyright (C) %(years)s Ryan Kavanagh' % \
        {'years': ', '.join(years)},
u''
u'This program is free software: you can redistribute it and/or modify',
u'it under the terms of the GNU Affero General Public License as published by',
u'the Free Software Foundation, either version 3 of the License, or',
u'(at your option) any later version.',
u'',
u'This program is distributed in the hope that it will be useful,',
u'but WITHOUT ANY WARRANTY; without even the implied warranty of',
u'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the',
u'GNU Affero General Public License for more details.',
u'',
u'For more details and to obtain the source code, please follow',
u'<a href="/vote/copyright/">this link</a>.']
    return '<br>'.join(copyright_msg)
