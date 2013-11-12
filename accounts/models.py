# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ORGANIZATION_TYPES = (
        ('enterprise', 'Entreprise'),
        ('public', 'Collectivité/Organisme public'),
        ('individual', 'Particulier'),
        ('independent', 'Indépendant'),
    )

    is_provider = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    is_performer = models.BooleanField(default=False)
    organization_type = models.CharField(choices=ORGANIZATION_TYPES,
                                         max_length=32,
                                         blank=True)
    organization_activity_field = models.CharField(max_length=50, blank=True)
    organization_name = models.CharField(max_length=100, blank=True)
    organization_address = models.CharField(max_length=100, blank=True)
    organization_post_code = models.CharField(max_length=20, blank=True)
    organization_town = models.CharField(max_length=100, blank=True)
    organization_url = models.URLField(blank=True)

    phone_number = models.CharField(max_length=50, blank=True)
