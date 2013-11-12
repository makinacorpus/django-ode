from django import forms

from frontend.models import User
from frontend.widgets import CheckboxInput, TextInput, Select


class SignupForm(forms.ModelForm):
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
            'password',
        ]
        widgets = {}
        for field in fields:
            if field.startswith('is_'):
                widgets[field] = CheckboxInput
            else:
                widgets[field] = TextInput
        widgets['organization_type'] = Select
