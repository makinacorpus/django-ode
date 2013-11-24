from django.conf.urls import patterns, url
from frontend.views import sources
from frontend.views import events
from frontend.views import providers

urlpatterns = patterns(
    'frontend.views',
    url(r'^$', 'main.home', name='home'),
    url(r'^sources/create', sources.Form.as_view(), name='sources_create'),
    url(r'^sources', 'sources.list', name='sources_list'),
    url(r'^events/create', events.Form.as_view(), name='events_create'),
    url(r'^events', 'events.list', name='events_list'),
    url(r'^provider_list/', providers.ProviderListView.as_view(),
        name='provider_list'),
    url(r'^provider_json_list/', providers.ProviderJsonListView.as_view(),
        name='provider_json_list'),
)
