from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from frontend.views import sources, events, providers, consumers, imports


urlpatterns = patterns(
    'frontend.views',
    url(r'^$', 'main.home', name='home'),
    url(r'^sources/create/$', sources.Form.as_view(), name='sources_create'),
    url(r'^events/create/$', events.Form.as_view(), name='events_create'),
    url(r'^events/$', events.EventListView.as_view(), name='event_list'),
    url(r'^provider_list/$', providers.ProviderListView.as_view(),
        name='provider_list'),
    url(r'^provider_json_list/$', providers.ProviderJsonListView.as_view(),
        name='provider_json_list'),
    url(r'^provider/(?P<pk>.+)/$', providers.ProviderView.as_view(),
        name='provider'),
    url(r'^consumer_list/$', consumers.ConsumerListView.as_view(),
        name='consumer_list'),
    url(r'^consumer_json_list/$', consumers.ConsumerJsonListView.as_view(),
        name='consumer_json_list'),
    url(r'^consumer/(?P<pk>.+)/$', consumers.ConsumerView.as_view(),
        name='consumer'),

    url(r'^imports/$', imports.ImportView.as_view(), name='imports'),
    url(r'^sources/json/$', sources.SourceJsonListView.as_view(),
        name='source_json_list'),
    url(r'^events/json/$', events.EventJsonListView.as_view(),
        name='event_json_list'),

    url(r'^sources/delete_rows/$', sources.SourceDeleteRowsView.as_view(),
        name='source_delete_rows'),

    url(r'^eula/$', TemplateView.as_view(template_name="eula.html"),
        name='eula'),
    url(r'^api/(?P<path>.+)$', 'api_proxy.proxy_view', name='api_proxy'),
)
