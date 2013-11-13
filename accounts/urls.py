from django.conf.urls import patterns, url

from accounts import views


urlpatterns = patterns(
    '',
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^login/', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^confirm_email/(?P<confirmation_code>.+)/$',
        views.EmailConfirmationView.as_view(), name='confirm_email'),
    url(r'signup_success/', views.SignupSuccess.as_view(),
        name='signup_success'),
)
