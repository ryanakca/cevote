#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

def fill(candidates_per_group):
    Position(name="Président", amount_of_electees="1", weight="-10").save()
    Position(name="Vice-président", amount_of_electees="1", weight="-9").save()
    cats = ["Sportif", "Culturel", "Pastorale"]
    for c in cats:
        Position(name="Chef %s" % c, amount_of_electees="1", weight="-5").save()
        Position(name="Adjoint %s" % c, amount_of_electees="2", weight="0").save()
    first_names = ["Pierre", "Jean", "Jeanne", "Janice"]
    initials = ["A.", "D.", "G.", "F."]
    last_names = ["LaFureur", "Lamontagne", "LaRoche", "Le Sorbier"]
    for i in range(candidates_per_group):
        for p in Position.objects.all():
            Candidate(first_name=random.choice(first_names), \
                initial=random.choice(initials),\
                last_name=random.choice(last_names),\
                votes=random.randint(1,150),
                position=p).save()
