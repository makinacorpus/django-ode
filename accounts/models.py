# -*- encoding: utf-8 -*-
import random
import time
import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import mail
from django.conf import settings


class User(AbstractUser):
    ORGANIZATION_TYPES = (
        ('enterprise', 'Entreprise'),
        ('public', 'Collectivité/Organisme public'),
        ('individual', 'Particulier'),
        ('independent', 'Indépendant'),
    )

    is_provider = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    is_performer = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    is_media = models.BooleanField(default=False)
    media_url = models.URLField(blank=True)
    is_website = models.BooleanField(default=False)
    website_url = models.URLField(blank=True)
    is_mobile_app = models.BooleanField(default=False)
    mobile_app_name = models.CharField(max_length=100, blank=True)
    is_other = models.BooleanField(default=False)
    other_details = models.CharField(max_length=100, blank=True)
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
    confirmation_code = models.CharField(max_length=40)

    def generate_confirmation_code(self):
        source = "{}:{}:{}".format(
            time.time(),
            self.username,
            random.randint(100000, 2000000),
        ).encode('utf-8')
        self.confirmation_code = hashlib.sha1(source).hexdigest()
        return self.confirmation_code

    def send_confirmation_email(self, confirmation_url):
        mail.send_mail(
            subject='Veuillez confirmer votre adresse email',
            message="""
            Veuillez cliquer sur ce lien de confirmation: {}
            """.format(confirmation_url),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=False)

# Override attributes of fields defined in AbstractUser
User._meta.get_field('is_active').default = False
User._meta.get_field('email').blank = False
