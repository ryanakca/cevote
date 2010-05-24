#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Randomly fills the database with candidates and positions.
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

import random
import sys
import os

sys.path.insert(0, os.curdir)

import settings
from vote.models import Position, Candidate

def fill(candidates_per_group):
    Position(name="Président", amount_of_electees="1", weight="-10").save()
    Position(name="Vice-président", amount_of_electees="1", weight="-9").save()
    cats = ["Sportif", "Culturel", "Pastorale"]
    for c in cats:
        Position(name="Chef %s" % c, amount_of_electees="1", weight="-5").save()
        Position(name="Adjoint %s" % c, amount_of_electees="2", weight="0").save()
    first_names = ["Pierre", "Jean", "Jeanne", "Janice"]
    last_names = ["LaFureur", "Lamontagne", "LaRoche", "Le Sorbier"]
    for i in range(candidates_per_group):
        for p in Position.objects.all():
            Candidate(first_name=random.choice(first_names), \
                last_name=random.choice(last_names),\
                votes=random.randint(1,150),
                position=p).save()

if __name__ == "__main__":
    fill(4)
