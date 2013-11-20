from django.conf.urls import patterns, url

from accounts import views
from accounts.forms import CustomAuthenticationForm


urlpatterns = patterns(
    '',
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^login/', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html',
        'authentication_form': CustomAuthenticationForm}, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^confirm_email/(?P<confirmation_code>.+)/$',
        views.EmailConfirmationView.as_view(), name='confirm_email'),
    url(r'signup_success/', views.SignupSuccess.as_view(),
        name='signup_success'),
    url(r'profile/', views.ProfileView.as_view(), name='profile'),
)
