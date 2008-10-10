from django.db import models
from django_extensions.db.fields import UUIDField

# Create your models here.
class Voter(models.Model):
    """ This class represents voters. Each voter is identified by a UUID and can
    be part of multiple groups. The boolean has_voted provides a mechanism to
    provide the voter from voting twice.
    """

    uuid = UUIDField("UUID")
    has_voted = models.BooleanField("Has voted?",False)

    def __init__(self):
        self.uuid.create_uuid()

    def __unicode__(self):
        return self.uuid

class Group(models.Model):
    """ This class represents a group of Voters. Each group has a name and can
    vote for certain positions. Certain groups can only cast half a vote. We'll
    ask what percentage of a vote this group can cast.
    """

    name = models.CharField("Group name", max_length=200)
    voters = models.ManyToManyField(Voter)
    vote_percentage = models.IntegerField("Percent of a vote this group can \
    cast", default=1.00)

    def __unicode__(self):
        return self.name

    def create_voter(self):
        self.voter.create()

class Candidate(models.Model):
    """ This class represents a Candidate. Each candidate has a firstname, an
    initial in for the occasion of two voters with the same firstname &
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
        return self.firstname + self.initial + self.last_name

class Position(models.Model):
    """ This class represents a position. It has a name and the required
    amount of people required to fill a position. voting_groups represents the
    groups of voters that can vote for this position.
    """

    name = models.CharField(max_length=200)
    amount_of_electees = models.IntegerField("Amount of electees required to \
    fill this position")
    voting_groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return self.name
