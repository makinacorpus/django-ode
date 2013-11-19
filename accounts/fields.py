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
        kwargs.setdefault('label', '')
        super(OrganizationTypeField, self).__init__(*args, **kwargs)


class OrganizationActivityFieldField(StandardCharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _("Domaine d'activité"))
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
