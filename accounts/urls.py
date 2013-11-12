from django.conf.urls import patterns, url

from accounts.views import SignupView


urlpatterns = patterns(
    '',
    url(r'^signup/', SignupView.as_view(), name='signup'),
)
