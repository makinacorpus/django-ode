from django import forms


class Select(forms.Select):

    def __init__(self, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control'}


class TextInput(forms.TextInput):

    def __init__(self, *args, **kwargs):
        super(TextInput, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control'}


class CheckboxInput(forms.CheckboxInput):

    def __init__(self, *args, **kwargs):
        super(CheckboxInput, self).__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control'}
