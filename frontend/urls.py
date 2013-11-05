from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'', 'frontend.views.home', name='home'),
)
