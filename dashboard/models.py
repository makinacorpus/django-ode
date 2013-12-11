# -*- encoding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB
#   access
# Feel free to rename the models, but don't rename db_table values or field
# names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom
# [appname]' into your database.
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CategoryAssociation(models.Model):
    tag = models.ForeignKey('Tag', blank=True, null=True)
    event = models.ForeignKey('Event', blank=True, null=True)

    class Meta:
        db_table = 'category_association'


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=1000)
    firstname = models.CharField(max_length=1000, blank=True,
                                 verbose_name=_("Prénom"))
    lastname = models.CharField(max_length=1000, blank=True,
                                verbose_name=_("Nom de famille"))
    email = models.CharField(max_length=1000, blank=True)
    telephone = models.CharField(max_length=1000, blank=True,
                                 verbose_name=_("Téléphone"))
    description = models.CharField(max_length=1000, blank=True,
                                   verbose_name=_("Description"))
    language = models.CharField(max_length=1000, blank=True)
    latlong = models.CharField(max_length=1000, blank=True)
    organiser = models.CharField(max_length=1000, blank=True)
    performers = models.CharField(max_length=1000, blank=True,
                                  verbose_name=_("Artistes, intervenants"))
    press_url = models.CharField(max_length=1000, blank=True)
    price_information = models.CharField(max_length=1000, blank=True,
                                         verbose_name=_("Tarif"))
    source = models.CharField(max_length=1000, blank=True)
    source_id = models.CharField(max_length=1000, blank=True)
    target = models.CharField(max_length=1000, blank=True,
                              verbose_name=_("Audience"))
    title = models.CharField(max_length=1000, blank=True,
                             verbose_name=_("Titre"))
    url = models.CharField(max_length=1000, blank=True)
    provider_id = models.CharField(max_length=1000, blank=True)
    start_time = models.DateTimeField(blank=True, null=True,
                                      verbose_name=_("Début"))
    end_time = models.DateTimeField(blank=True, null=True,
                                    verbose_name=_("Fin"))
    publication_start = models.DateTimeField(blank=True, null=True,
                                             verbose_name=_("Publication"))
    publication_end = models.DateTimeField(blank=True, null=True,
                                           verbose_name=_("Expiration"))
    press_contact_email = models.CharField(max_length=1000, blank=True,
                                           verbose_name=_("Email"))
    press_contact_name = models.CharField(max_length=1000, blank=True,
                                          verbose_name=_("Nom"))
    press_contact_phone_number = models.CharField(max_length=1000, blank=True,
                                                  verbose_name=_("Téléphone"))
    ticket_contact_email = models.CharField(max_length=1000, blank=True,
                                            verbose_name=_("Email"))
    ticket_contact_name = models.CharField(max_length=1000, blank=True,
                                           verbose_name=_("Nom"))
    ticket_contact_phone_number = models.CharField(max_length=1000, blank=True,
                                                   verbose_name=_("Téléphone"))
    tags = models.ManyToManyField('Tag', through='TagAssociation',
                                  related_name='tagged_events')
    categories = models.ManyToManyField('Tag', through='CategoryAssociation',
                                        related_name='categorized_events')

    class Meta:
        verbose_name = _("Événement")
        db_table = 'events'


class Location(models.Model):
    name = models.CharField(max_length=1000, blank=True,
                            verbose_name=_("Nom"))
    address = models.CharField(max_length=1000, blank=True,
                               verbose_name=_("Adresse"))
    post_code = models.CharField(max_length=1000, blank=True,
                                 verbose_name=_("Code postal"))
    capacity = models.CharField(max_length=1000, blank=True,
                                verbose_name=_("Capacité de la salle"))
    town = models.CharField(max_length=1000, blank=True,
                            verbose_name=_("Commune"))
    country = models.CharField(max_length=1000, blank=True,
                               verbose_name=_("Pays"))
    event = models.ForeignKey(Event, blank=True, null=True)

    class Meta:
        verbose_name = _("Lieu")
        managed = False
        db_table = 'locations'


class Media(models.Model):

    id = models.IntegerField(primary_key=True)
    event = models.ForeignKey(Event, blank=True, null=True)
    license = models.CharField(max_length=20, blank=True)
    url = models.CharField(max_length=1000, blank=True)
    type = models.CharField(max_length=20, blank=True)

    class Meta:
        managed = False
        db_table = 'media'


class Source(models.Model):

    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=1000, blank=True)
    active = models.NullBooleanField()
    provider_id = models.CharField(max_length=1000, blank=True)

    class Meta:
        managed = True
        db_table = 'sources'


class TagAssociation(models.Model):
    tag = models.ForeignKey('Tag', blank=True, null=True)
    event = models.ForeignKey(Event, blank=True, null=True)

    class Meta:
        db_table = 'tag_association'


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=True)

    class Meta:
        db_table = 'tags'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
