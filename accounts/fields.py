# -*- encoding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts import widgets as custom_widgets
from accounts.models import Organization


class Password1Field(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Password"))
        kwargs.setdefault('widget', custom_widgets.PasswordInput)
        kwargs.setdefault('min_length', 6)
        super(Password1Field, self).__init__(*args, **kwargs)


class Password2Field(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Password confirmation"))
        kwargs.setdefault('widget', custom_widgets.PasswordInput)
        kwargs.setdefault(
            'help_text',
            _("Enter the same password as above, for verification."))
        kwargs.setdefault('label', _('Confirmation du mot de passe'))
        super(Password2Field, self).__init__(*args, **kwargs)


class StandardCharField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 100)
        kwargs.setdefault('required', False)
        kwargs.setdefault('widget', custom_widgets.TextInput)
        super(StandardCharField, self).__init__(*args, **kwargs)


class OrganizationTypeField(forms.ChoiceField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', Organization.TYPES)
        kwargs.setdefault('required', False)
        kwargs.setdefault('label', _(u"Type de structure"))
        kwargs.setdefault('widget', custom_widgets.Select)
        super(OrganizationTypeField, self).__init__(*args, **kwargs)


class OrganizationActivityFieldField(StandardCharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _(u"Domaine d'activité"))
        super(OrganizationActivityFieldField, self).__init__(*args, **kwargs)


class OrganizationAddressField(StandardCharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Adresse"))
        super(OrganizationAddressField, self).__init__(*args, **kwargs)


class OrganizationPostCodeField(StandardCharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Code Postal"))
        super(OrganizationPostCodeField, self).__init__(*args, **kwargs)


class OrganizationTownField(StandardCharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Ville"))
        super(OrganizationTownField, self).__init__(*args, **kwargs)


class OrganizationNameField(StandardCharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Nom structure"))
        super(OrganizationNameField, self).__init__(*args, **kwargs)


class OrganizationURLField(forms.URLField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Site Internet"))
        kwargs.setdefault('required', False)
        kwargs.setdefault('widget', custom_widgets.TextInput)
        super(OrganizationURLField, self).__init__(*args, **kwargs)


class OrganizationIsProviderField(forms.BooleanField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _(u"Fournisseur de données"))
        kwargs.setdefault('widget', custom_widgets.IsProviderCheckboxInput)
        kwargs.setdefault('required', False)
        super(OrganizationIsProviderField, self).__init__(*args, **kwargs)


class OrganizationIsConsumerField(forms.BooleanField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _(u"Réutilisateur de données"))
        kwargs.setdefault('widget', custom_widgets.IsConsumerCheckboxInput)
        kwargs.setdefault('required', False)
        super(OrganizationIsConsumerField, self).__init__(*args, **kwargs)


class SimpleCheckboxField(forms.BooleanField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', custom_widgets.CheckboxInput)
        kwargs.setdefault('required', False)
        super(SimpleCheckboxField, self).__init__(*args, **kwargs)


class OrganizationIsHostField(SimpleCheckboxField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _(u"Lieu d'accueil d'événements"))
        super(OrganizationIsHostField, self).__init__(*args, **kwargs)


class OrganizationIsPerformerField(SimpleCheckboxField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _(u"Intervenant/artiste"))
        super(OrganizationIsPerformerField, self).__init__(*args, **kwargs)


class OrganizationIsMediaField(SimpleCheckboxField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Publication d'un media print/web"))
        super(OrganizationIsMediaField, self).__init__(*args, **kwargs)


class OrganizationIsCreatorField(SimpleCheckboxField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _(u"Créateur d'événements"))
        super(OrganizationIsCreatorField, self).__init__(*args, **kwargs)


class OrganizationIsWebsiteField(SimpleCheckboxField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Site web"))
        super(OrganizationIsWebsiteField, self).__init__(*args, **kwargs)


class OrganizationIsMobileAppField(SimpleCheckboxField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Application mobile"))
        super(OrganizationIsMobileAppField, self).__init__(*args, **kwargs)


class OrganizationIsOtherField(SimpleCheckboxField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Autre"))
        super(OrganizationIsOtherField, self).__init__(*args, **kwargs)


class OrganizationMediaURLField(forms.URLField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', "")
        kwargs.setdefault('required', False)
        kwargs.setdefault('widget', custom_widgets.TextInput)
        super(OrganizationMediaURLField, self).__init__(*args, **kwargs)


class OrganizationWebsiteURLField(forms.URLField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', "")
        kwargs.setdefault('required', False)
        kwargs.setdefault('widget', custom_widgets.TextInput)
        super(OrganizationWebsiteURLField, self).__init__(*args, **kwargs)
