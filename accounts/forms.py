from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import User
from accounts.widgets import CheckboxInput, TextInput, Select


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'is_provider',
            'is_consumer',
            'is_host',
            'is_creator',
            'is_performer',
            'organization_type',
            'organization_activity_field',
            'organization_name',
            'organization_address',
            'organization_post_code',
            'organization_town',
            'organization_url',
            'last_name',
            'first_name',
            'email',
            'phone_number',
            'username',
        ]
        widgets = {}
        for field in fields:
            if field.startswith('is_'):
                widgets[field] = CheckboxInput
            else:
                widgets[field] = TextInput
        widgets['organization_type'] = Select

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
