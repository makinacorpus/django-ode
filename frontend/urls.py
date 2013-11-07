from django.conf.urls import patterns, url

urlpatterns = patterns(
    'frontend.views',
    url(r'^$', 'main.home', name='home'),
    url(r'^sources/create', 'sources.create', name='create'),
    url(r'^sources', 'sources.list', name='list'),
)
