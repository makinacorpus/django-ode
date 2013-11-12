from django.views.generic import CreateView
from accounts.forms import SignupForm


class SignupView(CreateView):

    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = '/accounts/profile/'
