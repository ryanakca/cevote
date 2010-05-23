# Voter ID Field
# Copyright (C) 2010  Ryan Kavanagh <ryanakca@kubuntu.org>
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

from django.db.models.fields import CharField
from datetime import datetime
from random import randint
import string

def ToBase62(number):
    ''' Convert positive integer to a base62 string. '''

    alphabet = string.letters + string.digits

    if not isinstance(number, (int, long)):
        raise TypeError('Number must be an integer')
    if number < 0:
        raise ValueError('Number must be positive')

    if number < 62:
        return alphabet[number]

    base62 = ''
    while number != 0:
        number, i = divmod(number, 62)
        base62 = alphabet[i] + base62
    return base62


class VIDField(CharField):
    """ Voter ID Field. """
    def __init__(self, **kwargs):
        kwargs['max_length'] = 15
        CharField.__init__(self, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def pre_save(self, model_instance, add):
        if add:
            randomint = int(str(datetime.utcnow())[-6:]) * random.randint(100,
                        10000) * random.randint(100, 10000)
            return unicode(ToBase62(randomint))
        else:
            return super(CharField, self).pre_save(model_instance, add)
