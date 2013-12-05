from django import forms


class Select(forms.Select):

    def __init__(self, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control'}


class TextInput(forms.TextInput):

    def __init__(self, *args, **kwargs):
        super(TextInput, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control'}


class EmailInput(forms.TextInput):

    def __init__(self, *args, **kwargs):
        super(EmailInput, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control'}


class PasswordInput(forms.PasswordInput):

    def __init__(self, *args, **kwargs):
        super(PasswordInput, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control'}


class CheckboxInput(forms.CheckboxInput):

    def __init__(self, *args, **kwargs):
        super(CheckboxInput, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control'}


class CollapseCheckboxInput(CheckboxInput):

    def __init__(self, *args, **kwargs):
        super(CollapseCheckboxInput, self).__init__(*args, **kwargs)
        self.attrs['data-toggle'] = 'collapse'


class IsProviderCheckboxInput(CollapseCheckboxInput):

    def __init__(self, *args, **kwargs):
        super(IsProviderCheckboxInput, self).__init__(*args, **kwargs)
        self.attrs['data-target'] = '#is-provider-details'


class IsConsumerCheckboxInput(CollapseCheckboxInput):

    def __init__(self, *args, **kwargs):
        super(IsConsumerCheckboxInput, self).__init__(*args, **kwargs)
        self.attrs['data-target'] = '#is-consumer-details'
