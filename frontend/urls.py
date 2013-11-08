from django.conf.urls import patterns, url
from frontend.views import sources
from frontend.views import events

urlpatterns = patterns(
    'frontend.views',
    url(r'^$', 'main.home', name='home'),
    url(r'^sources/create', sources.Form.as_view(), name='sources_create'),
    url(r'^sources', 'sources.list', name='sources_list'),
    url(r'^events/create', events.Form.as_view(), name='events_create'),
)
