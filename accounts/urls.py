from django.conf.urls import patterns, url

from accounts.views import SignupView, EmailConfirmationView


urlpatterns = patterns(
    '',
    url(r'^signup/', SignupView.as_view(), name='signup'),
    url(r'^confirm_email/(?P<confirmation_code>.+)/$',
        EmailConfirmationView.as_view(), name='signup'),
)
