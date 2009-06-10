#
# Models used for the voting application
# Copyright (C) 2008, 2009  Ryan Kavanagh <ryanakca@kubuntu.org>
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
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from cevote.vote.UUIDField import UUIDField

# Create your models here.
class Group(models.Model):
    """
    This class represents a group of Voters.

    @type name: str
    @ivar name: Name of the group of Voters
    @type vote_percentage: int
    @type vote_percentage: The percentage of a vote this group can cast
    """

    name = models.CharField(_("Group name"), max_length=200)
    vote_percentage = models.IntegerField(_("Percent of a vote this group " \
        "can cast"), default=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Voter group")
        verbose_name_plural = _("Voter groups")

class Voter(models.Model):
    """
    This class represents voters.

    @type has_voted: bool
    @ivar has_voted: Wether the voter has voted
    @type user: User
    @ivar user: The Django User model
    @type group: Group
    @ivar group: The voting group
    """

    uuid = UUIDField(_("UUID"),version=4)
    has_voted = models.BooleanField(_("Has voted?"),default=False)
    user = models.ForeignKey(User,unique=True)
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return str(self.uuid)[:15]

    class Meta:
        verbose_name = _("Voter")
        verbose_name_plural = _("Voters")

class Position(models.Model):
    """ 
    This class represents an electoral position.

    @type name: str
    @ivar name: Name of the position
    @type amount_of_electees: int
    @ivar amount_of_electees: Number of electees required to fill this position
    @type voting_groups: Group
    @ivar voting_group: Groups which may vote for this position
    @type weight: int
    @ivar weight: Location of this position on the voter's ballot. The lower
    the lighter / higher on the ballot.
    """

    name = models.CharField(max_length=200)
    amount_of_electees = models.IntegerField(_("Number of electees " \
        "required to fill this position"))
    voting_groups = models.ManyToManyField(Group)
    weight = models.IntegerField(_("Location of this field on the " \
        "voter's ballot"), default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['weight',]
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")


class Candidate(models.Model):
    """
    This class represents a candidate.

    @type first_name: str
    @ivar first_name: The candidate's first_name
    @type initial: str
    @ivar initial: The candidate's initial
    @type last_name: str
    @ivar last_name: The candidate's last name
    @type position: Position
    @ivar position: Position this candidate is running for.
    @type picture: str
    @ivar picture: Path to picture
    @type votes: int
    @ivar votes: The number of votes this candidate has won.
    """

    first_name = models.CharField(max_length=50)
    initial = models.CharField(max_length=5)
    last_name = models.CharField(max_length=75)
    position = models.ForeignKey(Position)
    picture = models.ImageField(upload_to='vote/candidate_pictures/', blank=True)
    votes = models.FloatField(default=0)

    def __unicode__(self):
        return "%s, %s %s" % (self.last_name.upper(), self.first_name,  self.initial)

    class Meta:
        verbose_name = _("Candidate")
        verbose_name_plural = _("Candidates")
        ordering = ['votes',]

class ElectionDateTime(models.Model):
    """
    This class represents the date / time where users may vote.
    
    @type start: datetime
    @ivar start: Time where the elections start
    @type end: datetime
    @ivar end: Time when the elections end
    """

    start = models.DateTimeField(_("Election start date/time."))
    end = models.DateTimeField(_("Election end date/time."))

    def __unicode__(self):
        return "%s--%s" % (self.start, self.end)

    class Meta:
        verbose_name = _("Election times")
        verbose_name_plural = verbose_name
        ordering = ['start']
