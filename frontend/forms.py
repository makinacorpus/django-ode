from django import forms

from frontend.models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'is_provider',
            'is_consumer',
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
        ]
