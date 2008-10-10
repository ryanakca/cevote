from cevote.voting.models import Voter, Group, Candidate, Position
from django.contrib import admin

class VoterAdmin(admin.ModelAdmin):
   exclude = ['has_voted',]
   list_filter = ['groups',]


class GroupAdmin(admin.ModelAdmin):
    model = Voter

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 3

class CandidateAdmin(admin.ModelAdmin):
    inital.width = 20
class PositionAdmin(admin.ModelAdmin):
    inlines = [CandidateInline,]

admin.site.register(Voter, VoterAdmin)
admin.site.register(Group)
admin.site.register(Candidate)
admin.site.register(Position, PositionAdmin)
