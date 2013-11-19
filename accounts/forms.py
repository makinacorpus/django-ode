from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from accounts.models import User
from accounts import widgets as custom_widgets
from accounts import fields


class SignupForm(UserCreationForm):

    username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")},
        widget=custom_widgets.TextInput,
        label=_("Identifiant"))

    password1 = fields.Password1Field(label=_('Mot de passe'))
    password2 = fields.Password2Field()

    organization_activity_field = fields.OrganizationActivityFieldField()
    organization_name = fields.OrganizationNameField()
    organization_price_information = forms.CharField(
        max_length=100, required=False, widget=custom_widgets.TextInput)
    organization_type = fields.OrganizationTypeField()
    organization_address = fields.OrganizationAddressField()
    organization_post_code = fields.OrganizationPostCodeField()
    organization_town = fields.OrganizationTownField()
    organization_url = fields.OrganizationURLField()

    accept_terms_of_service = forms.BooleanField(
        widget=custom_widgets.CheckboxInput
    )

    class Meta:
        model = User
        fields = [
            'is_provider',
            'is_host',
            'is_creator',
            'is_performer',
            'is_consumer',
            'is_media',
            'is_website',
            'is_mobile_app',
            'mobile_app_name',
            'is_other',
            'other_details',
            'website_url',
            'media_url',
            'last_name',
            'first_name',
            'email',
            'phone_number',
            'username',
        ]
        widgets = {}
        for field in fields:
            if field.startswith('is_'):
                widgets[field] = custom_widgets.CheckboxInput
            else:
                widgets[field] = custom_widgets.TextInput
        widgets['organization_type'] = custom_widgets.Select
        widgets['is_provider'] = custom_widgets.IsProviderCheckboxInput
        widgets['is_consumer'] = custom_widgets.IsConsumerCheckboxInput

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class ProfileForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta:
        model = User
        fields = []

    password1 = fields.Password1Field(required=False, label=_('Mot de passe'))
    password2 = fields.Password2Field(required=False)

    organization_name = fields.OrganizationNameField()
    organization_type = fields.OrganizationTypeField()
    organization_activity_field = fields.OrganizationActivityFieldField()
    organization_address = fields.OrganizationAddressField()
    organization_post_code = fields.OrganizationPostCodeField()
    organization_town = fields.OrganizationTownField()
    organization_url = fields.OrganizationURLField()

    # Infos générales événements
    organization_price_information = fields.StandardCharField(label=_("Tarif"))
    organization_audience = fields.StandardCharField(label=_("Public"))
    organization_capacity = fields.StandardCharField(
        label=_("Capacité de la salle"))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        if self.cleaned_data['password1']:
            self.user.set_password(self.cleaned_data['password1'])
        if commit:
            self.user.save()
        return self.user
