from django.conf.urls import patterns, url
from frontend.views import sources, events, providers, consumers

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
    url(r'^consumer_list/', consumers.ConsumerListView.as_view(),
        name='consumer_list'),
    url(r'^consumer_json_list/', consumers.ConsumerJsonListView.as_view(),
        name='consumer_json_list'),
)
