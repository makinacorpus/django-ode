from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from accounts.models import User
from accounts.widgets import CheckboxInput, TextInput, Select, PasswordInput


class SignupForm(UserCreationForm):

    username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")},
        widget=TextInput)

    password1 = forms.CharField(label=_("Password"),
                                widget=PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

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
