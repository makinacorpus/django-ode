# -*- encoding: utf-8 -*-
from django.core import mail
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm, ProfileForm
from accounts.models import User


class SignupView(CreateView):

    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = '/accounts/signup_success/'

    def get_success_url(self):
        success_url = super(SignupView, self).get_success_url()
        if self.object.is_provider:
            success_url += '?is_provider=True'
        return success_url

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        user = form.save(commit=False)
        confirmation_code = user.generate_confirmation_code()
        confirmation_path = reverse('accounts:confirm_email', kwargs={
            'confirmation_code': confirmation_code
        })
        confirmation_url = self.request.build_absolute_uri(confirmation_path)
        user.send_confirmation_email(confirmation_url)
        user.save()
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class EmailConfirmationView(TemplateView):

    template_name = 'accounts/email_confirmation.html'

    def activate_user(self, user):
        user.is_active = True
        user.save()

    def send_moderation_request_email(self, user):
        path = reverse('admin:accounts_user_change', args=(user.id, ))
        url = self.request.build_absolute_uri(path)
        mail.send_mail(
            subject=u"Nouveau fournisseur de données",
            message=u"Validez ce fournisseur: %s" % url,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ACCOUNTS_MODERATOR_EMAILS,
            fail_silently=False)

    def get(self, request, confirmation_code, *args, **kwargs):
        try:
            user = User.objects.get(confirmation_code=confirmation_code)
            if user.is_provider:
                self.send_moderation_request_email(user)
            else:
                self.activate_user(user)
            self.success = True
        except User.DoesNotExist:
            self.success = False
        return super(EmailConfirmationView, self).get(request, *args, **kwargs)


class SignupSuccess(TemplateView):

    template_name = 'accounts/signup_success.html'


class ProfileView(UpdateView):

    template_name = 'accounts/profile.html'
    form_class = ProfileForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user
