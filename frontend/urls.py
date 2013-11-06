from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'frontend.views.main.home', name='home'),
    url(r'^sources/new', 'frontend.views.sources.new', name='new_source'),
)
