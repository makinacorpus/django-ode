# -*- encoding: utf-8 -*-
import random
import time
import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name


class Organization(models.Model):
    class Meta:
        verbose_name = _("Structure")
    TYPES = (
        (u'enterprise', _(u'Entreprise')),
        (u'public', _(u'Collectivité/Organisme public')),
        (u'individual', _(u'Particulier')),
        (u'independent', _(u'Indépendant')),
        (u'non-profit', _(u'Association')),
    )

    PROVIDERS = (
        (u'host', _(u"Lieu d'accueil d'événements")),
        (u'performer', _(u"Intervenant/artiste")),
        (u'creator', _(u"Créateur d'événements")),
        )

    CONSUMERS = (
        (u'media', _(u"Publication d'un media print/web")),
        (u'website', _(u"Site web")),
        (u'mobile_app', _(u"Application mobile")),
        (u'other', _(u"Autre")),
        )

    PROVIDERS_DICT = dict(PROVIDERS)
    CONSUMERS_DICT = dict(CONSUMERS)

    name = models.CharField(max_length=100, blank=True, verbose_name=_("Nom"))
    picture = models.ImageField(upload_to="organization/profile_picture",
                                verbose_name=_("Image"))
    activity_field = models.CharField(max_length=50, blank=True,
                                      verbose_name=_(u"Domaine d'activité"))
    type = models.CharField(choices=TYPES, max_length=32, blank=True)
    address = models.CharField(max_length=100, blank=True,
                               verbose_name=_("Adresse"))
    post_code = models.CharField(max_length=20, blank=True,
                                 verbose_name=_("Code postal"))
    town = models.CharField(max_length=100, blank=True,
                            verbose_name=_("Commune"))
    url = models.URLField(blank=True, verbose_name=_(u"Site web"))
    is_provider = models.BooleanField(
        default=False,
        verbose_name=_(u"Fournisseur de données"))
    is_consumer = models.BooleanField(
        default=False,
        verbose_name=_(u"Réutilisateur de données"))
    is_host = models.BooleanField(default=False,
                                  verbose_name=PROVIDERS_DICT['host'])
    is_creator = models.BooleanField(default=False,
                                     verbose_name=PROVIDERS_DICT['creator'])
    is_performer = models.BooleanField(
        default=False,
        verbose_name=PROVIDERS_DICT['performer'])
    is_media = models.BooleanField(default=False,
                                   verbose_name=CONSUMERS_DICT['media'])
    is_website = models.BooleanField(default=False,
                                     verbose_name=CONSUMERS_DICT['website'])
    is_mobile_app = models.BooleanField(
        default=False,
        verbose_name=CONSUMERS_DICT['mobile_app'])
    is_other = models.BooleanField(default=False,
                                   verbose_name=CONSUMERS_DICT['other'])
    media_url = models.URLField(blank=True, verbose_name=_("URL media"))
    website_url = models.URLField(blank=True, verbose_name=_("URL site web"))
    mobile_app_name = models.CharField(max_length=100, blank=True,
                                       verbose_name=_("Nom appli mobile"))
    other_details = models.CharField(max_length=100, blank=True,
                                     verbose_name=_(u"Autres détails"))
    # Event related
    price_information = models.CharField(max_length=100, blank=True,
                                         verbose_name=_("Tarif"))
    audience = models.CharField(max_length=100, blank=True,
                                verbose_name=_("Public"))
    capacity = models.CharField(max_length=100, blank=True,
                                verbose_name=_(u"Capacité du lieu"))
    ticket_contact = models.ForeignKey(Contact, null=True,
                                       related_name='ticket_organization',
                                       verbose_name=_("Contact Billetterie"))
    press_contact = models.ForeignKey(Contact, null=True,
                                      related_name='press_organization',
                                      verbose_name=_("Contact Presse"))
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

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class User(AbstractUser):
    organization = models.ForeignKey(Organization, null=True)

    phone_number = models.CharField(max_length=50, blank=True,
                                    verbose_name=_(u"Téléphone"))
    confirmation_code = models.CharField(max_length=40)

    # This field is only used to know if its first user inscription
    first_inscription = models.BooleanField(default=True, editable=False)

    def generate_confirmation_code(self):
        source = "{}:{}:{}".format(
            time.time(),
            self.username,
            random.randint(100000, 2000000),
        ).encode('utf-8')
        self.confirmation_code = hashlib.sha1(source).hexdigest()
        return self.confirmation_code

    def send_confirmation_email(self, confirmation_url):
        message = render_to_string(
            'accounts/email_activation.html',
            {'confirm_link': confirmation_url})
        mail.send_mail(
            subject=_(u"Ouverture d'un compte sur www.opendataevents.fr"),
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=False)

    def save(self, *args, **kwargs):

        super(User, self).save(*args, **kwargs)

        if self.organization:
            user_is_prov = self.organization.is_provider

            # This case manage the first admin manual activation
            # for provider inscription
            # In that case, we send an email to provider, so that he can
            # know that its inscription is validated
            if self.first_inscription and self.is_active and user_is_prov:
                self.first_inscription = False
                message = render_to_string(
                    'accounts/email_provider_validation.html')
                sub = _(u"Votre compte a été validé sur www.opendataevents.fr")
                mail.send_mail(
                    subject=sub,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.email],
                    fail_silently=False)
                self.save()


# Override attributes of fields defined in AbstractUser
User._meta.get_field('is_active').default = False
User._meta.get_field('email').blank = False
User._meta.get_field('email').verbose_name = _(u"Email ")
