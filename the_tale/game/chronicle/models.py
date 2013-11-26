# coding: utf-8

from django.db import models

from rels.django import TableIntegerField

from the_tale.game.chronicle.relations import RECORD_TYPE, ACTOR_ROLE


class Actor(models.Model):

    MAX_UID_LENGTH = 16

    uid = models.CharField(max_length=MAX_UID_LENGTH, unique=True)

    bill = models.ForeignKey('bills.Bill', null=True, related_name='+', on_delete=models.SET_NULL)
    place = models.ForeignKey('places.Place', null=True, related_name='+', on_delete=models.SET_NULL)
    person = models.ForeignKey('persons.Person', null=True, related_name='+', on_delete=models.SET_NULL)

    def __unicode__(self):
        if self.bill_id is not None: return unicode(self.bill)
        if self.place_id is not None: return unicode(self.place)
        if self.person_id is not None: return unicode(self.person)


class Record(models.Model):

    type = TableIntegerField(relation=RECORD_TYPE, relation_column='value', db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_at_turn = models.IntegerField(null=False)

    text = models.TextField(null=False, blank=True)

    actors = models.ManyToManyField(Actor, through='RecordToActor')

    def __unicode__(self):
        return self.type.text


class RecordToActor(models.Model):

    role = TableIntegerField(relation=ACTOR_ROLE, relation_column='value')

    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.PROTECT)

    def __unicode__(self): return '<%d, %d>' % (self.record_id, self.actor_id)
