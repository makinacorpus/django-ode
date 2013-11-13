from django.views.generic import CreateView, TemplateView
from accounts.forms import SignupForm
from accounts.models import User


class SignupView(CreateView):

    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = '/accounts/profile/'


class EmailConfirmationView(TemplateView):

    template_name = 'accounts/email_confirmation.html'

    def get(self, request, confirmation_code, *args, **kwargs):
        try:
            user = User.objects.get(confirmation_code=confirmation_code)
            user.is_active = True
            user.save()
            self.success = True
        except User.DoesNotExist:
            self.success = False
        return super(EmailConfirmationView, self).get(request, *args, **kwargs)
