# Classes for the administrative interface
# Copyright (C) 2008  Ryan Kavanagh <ryanakca@kubuntu.org>
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
from cevote.voting.models import Candidate, Position, Voter, Group
from django.contrib import admin

class CandidateAdmin(admin.ModelAdmin):
    pass

class CandidateInline(admin.StackedInline):
    model = Candidate
    exclude = ['votes',]
    extra = 4

class PositionAdmin(admin.ModelAdmin):
    inlines = [CandidateInline,]

admin.site.register(Position, PositionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Group)
admin.site.register(Voter)
