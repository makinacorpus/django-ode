from django.conf.urls import patterns, url

from accounts import views
from accounts import forms


urlpatterns = patterns(
    '',
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^login/', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html',
         'authentication_form': forms.CustomAuthenticationForm}, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^confirm_email/(?P<confirmation_code>.+)/$',
        views.EmailConfirmationView.as_view(), name='confirm_email'),
    url(r'signup_success/', views.SignupSuccess.as_view(),
        name='signup_success'),
    url(r'profile/', views.ProfileView.as_view(), name='profile'),

    url(r'^password_reset/', 'django.contrib.auth.views.password_reset',
        {'template_name': 'accounts/password_reset.html',
         'email_template_name': 'accounts/email_password_reset.html',
         'password_reset_form': forms.CustomPasswordResetForm,
         'post_reset_redirect': '/accounts/password_reset_done/'},
        name='password_reset'),
    url(r'^password_reset_done/',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'accounts/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'accounts/password_reset_confirm.html',
         'set_password_form': forms.CustomSetPasswordForm,
         'post_reset_redirect': '/accounts/password_reset_complete/'},
        name='password_reset_confirm'),
    url(r'^password_reset_complete/',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'accounts/password_reset_complete.html'},
        name='password_reset_complete'),
)
