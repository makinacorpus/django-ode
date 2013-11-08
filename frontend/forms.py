from django import forms

from frontend.models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_provider', 'is_consumer']
