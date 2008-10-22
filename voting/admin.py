from cevote.voting.models import Candidate, Position
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
