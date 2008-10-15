from cevote.voting.models import Voter, Group, Candidate, Position
from django.contrib import admin

class VoterInline(admin.TabularInline):
    model = Voter
    exclude = ['has_voted',]

class GroupAdmin(admin.ModelAdmin):
    model = Group
    inline = ['VoterInline',]

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 3

class CandidateAdmin(admin.ModelAdmin):
    #inital.width = 20
    pass
    
class PositionAdmin(admin.ModelAdmin):
    inlines = ['CandidateInline',]

admin.site.register(Group, GroupAdmin)
admin.site.register(Candidate)
admin.site.register(Position, PositionAdmin)
