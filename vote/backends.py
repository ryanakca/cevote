# Voter Authentication Backend
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
from django.contrib.auth.models import User
from vote.models import Voter

class VoterBackend:
    """
    Authentication Backend for the Voter model that uses UUIDs.
    """

    def authenticate(self, uuid=None):
        """
        Custom authentication method using a UUID
    
        @type uuid: str
        @param uuid: Voter's UUID
        @rtype: User
        @return: authenticated user
        """

        try:
            voter = Voter.objects.get(uuid__startswith=uuid)
            if not voter.has_voted:
                return voter.user
            else:
                raise User.DoesNotExist
        except Voter.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Fetches requested user

        @type user_id: int
        @param user_id: Requested User object's ID
        @rtype: User
        @return: requested user
        """

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
