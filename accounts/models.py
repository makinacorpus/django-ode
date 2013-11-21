# -*- encoding: utf-8 -*-
import random
import time
import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import mail
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)


class Organization(models.Model):
    TYPES = (
        ('enterprise', 'Entreprise'),
        ('public', 'Collectivité/Organisme public'),
        ('individual', 'Particulier'),
        ('independent', 'Indépendant'),
    )

    name = models.CharField(max_length=100, blank=True)
    picture = models.ImageField(upload_to="organization/profile_picture")
    activity_field = models.CharField(max_length=50, blank=True,
                                      verbose_name=_(u"Domaine d'activité"))
    price_information = models.CharField(max_length=100, blank=True)
    audience = models.CharField(max_length=100, blank=True)
    capacity = models.CharField(max_length=100, blank=True)
    type = models.CharField(choices=TYPES, max_length=32, blank=True)
    address = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    town = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    is_provider = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    is_performer = models.BooleanField(default=False)
    is_media = models.BooleanField(default=False)
    is_website = models.BooleanField(default=False)
    is_mobile_app = models.BooleanField(default=False)
    is_other = models.BooleanField(default=False)
    media_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    mobile_app_name = models.CharField(max_length=100, blank=True)
    other_details = models.CharField(max_length=100, blank=True)
    ticket_contact = models.ForeignKey(Contact, null=True,
                                       related_name='ticket_organization')
    press_contact = models.ForeignKey(Contact, null=True,
                                      related_name='press_organization')
    CONTACT_TYPES = ('ticket_contact', 'press_contact')

    def update_contact_field(self, form_name, cleaned_data):
        for contact_type in self.CONTACT_TYPES:
            prefix = 'organization_{}_'.format(contact_type)
            if form_name.startswith(prefix):
                model_name = form_name.replace(prefix, '')
                contact = getattr(self, contact_type)
                setattr(contact, model_name, cleaned_data[form_name])
                return True

    def update(self, cleaned_data):
        for contact_type in self.CONTACT_TYPES:
            if not getattr(self, contact_type):
                setattr(self, contact_type, Contact.objects.create())

        for form_name in cleaned_data:
            if self.update_contact_field(form_name, cleaned_data):
                continue
            model_name = form_name.replace('organization_', '')
            setattr(self, model_name, cleaned_data[form_name])

        self.ticket_contact.save()
        self.press_contact.save()
        self.save()


class User(AbstractUser):
    organization = models.ForeignKey(Organization, null=True)

    phone_number = models.CharField(max_length=50, blank=True,
                                    verbose_name=_(u"Téléphone"))
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
User._meta.get_field('email').verbose_name = _(u"Email ")
