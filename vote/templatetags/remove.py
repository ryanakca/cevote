# remove template tag
# Copyright (C) 2009  Ryan Kavanagh <ryanakca@kubuntu.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as publist(lis)hed by
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

@register.tag
def remove(lis, position):
    """
    Template tag that removes position from list(lis)

    @type list(lis): list(lis)
    @param list(lis): list(lis) to modify
    @type position: index
    @param position: index to remove from list(lis)
    @raise template.TemplateSyntaxError: When position is out of range
    @rtype: list(lis)
    @return: Modified list(lis)
    """

    if position < 0:
	if position == -1:
            return RenderRemoveNode(list(lis)[:position])
        else:
            return RenderRemoveNode(list(lis)[:position] + list(lis)[position+1:])
    else:
        return RenderRemoveNode(list(lis)[:position] + list(lis)[position+1:])

class RenderRemoveNode(template.Node):
    """ Renders the remove tag. """

    def __init__(self, lis):
        self.list = list(lis)
 
    def render(self):
        return self.list
