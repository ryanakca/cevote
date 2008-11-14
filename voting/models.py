from django.db import models
from django_extensions.db.fields import UUIDField
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

# Create your models here.
class Voter(models.Model):
    """ This class represents voters. Each voter is identified by a UUID and can
    be part of multiple groups. The boolean has_voted provides a mechanism to
    provide the voter from voting twice.
    """

    uuid = UUIDField(_("UUID"),version=4)
    has_voted = models.BooleanField(_("Has voted?"),default=False)

    def __unicode__(self):
        return self.uuid

    class Meta:
        verbose_name = _("Voter")
        verbose_name_plural = _("Voters")

class Group(models.Model):
    """ This class represents a group of Voters. Each group has a name and can
    vote for certain positions. Certain groups can only cast half a vote. We'll
    ask what percentage of a vote this group can cast.
    """

    name = models.CharField(_("Group name"), max_length=200)
    voters = models.ManyToManyField(Voter)
    vote_percentage = models.IntegerField(_("Percent of a vote this group " \
        "can cast"), default=1.00)

    def __unicode__(self):
        return self.name

    def create_voters(self, number, *args):
        """ Creates number of Voter() with *args as its groups. """
        for v in range(number):
            v = Voter()
            v.save()
            for g in args:
                g.voters.add(v)
    create_voters.short_description = _("Create voters")

    class Meta:
        verbose_name = _("Voter group")
        verbose_name_plural = _("Voter groups")

class Position(models.Model):
    """ This class represents a position. It has a name and the required
    amount of people required to fill a position. voting_groups represents the
    groups of voters that can vote for this position.
    """

    name = models.CharField(max_length=200)
    amount_of_electees = models.IntegerField(_("Amount of electees " \
        "required to fill this position"))
    voting_groups = models.ManyToManyField(Group)
    weight = models.IntegerField(_("Location of this field on the " \
        "voter's balot"), default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['weight',]
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")


class Candidate(models.Model):
    """ This class represents a Candidate. Each candidate has a first_name, an
    initial in for the occasion of two voters with the same first_name &
    lastname, a lastname. Associated with a single position and a picture. Each
    candidate is also associated with the amount of votes aquired.
    """

    first_name = models.CharField(max_length=50)
    initial = models.CharField(max_length=5)
    last_name = models.CharField(max_length=75)
    position = models.ForeignKey(Position)
    picture = models.ImageField(upload_to='candidate_pictures', blank=True)
    votes = models.IntegerField()

    def __unicode__(self):
        return "%s, %s %s" % (self.last_name.upper(), self.first_name,  self.initial)

    class Meta:
        verbose_name = _("Candidate")
        verbose_name_plural = _("Candidates")
        ordering = ['votes',]
