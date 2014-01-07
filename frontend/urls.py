from django.conf.urls import patterns, url
from frontend.views import (
    sources, events, providers, consumers, imports, export
    )
from frontend.views import webservices


urlpatterns = patterns(
    'frontend.views',
    url(r'^$', 'main.home', name='home'),

    url(r'^events/create/$', events.Form.as_view(), name='event_create'),
    url(r'^events/edit/(?P<id>.+)/$', events.Form.as_view(),
        name='event_edit'),
    url(r'^events/$', events.EventListView.as_view(), name='event_list'),
    url(r'^events/user/$', events.EventListUserView.as_view(),
        name='event_list_user'),
    url(r'^events/json/$', events.EventJsonListView.as_view(),
        name='event_json_list'),
    url(r'^events/user/json/$', events.EventJsonListUserView.as_view(),
        name='event_json_list_user'),
    url(r'^events/delete_rows/$', events.EventsDeleteRowsView.as_view(),
        name='events_delete_rows'),
    url(r'^events/duplicate_rows/$', events.EventsDuplicateRowsView.as_view(),
        name='events_duplicate_rows'),
    url(r'^events/(?P<id>.+)/$', events.EventView.as_view(), name='event'),

    url(r'^provider_list/$', providers.ProviderListView.as_view(),
        name='provider_list'),
    url(r'^provider_export/$', providers.ProviderExportView.as_view(),
        name='provider_export'),
    url(r'^provider_json_list/$', providers.ProviderJsonListView.as_view(),
        name='provider_json_list'),
    url(r'^provider/(?P<pk>.+)/$', providers.ProviderView.as_view(),
        name='provider'),
    url(r'^consumer_list/$', consumers.ConsumerListView.as_view(),
        name='consumer_list'),
    url(r'^consumer_export/$', consumers.ConsumerExportView.as_view(),
        name='consumer_export'),
    url(r'^consumer_json_list/$', consumers.ConsumerJsonListView.as_view(),
        name='consumer_json_list'),
    url(r'^consumer/(?P<pk>.+)/$', consumers.ConsumerView.as_view(),
        name='consumer'),

    url(r'^imports/$', imports.ImportView.as_view(), name='imports'),
    url(r'^imports/file/$', imports.APIImportFileForm.as_view(),
        name='imports_file'),
    url(r'^imports/source/$', imports.APIImportSourceForm.as_view(),
        name='imports_source'),
    url(r'^export/$', export.ExportView.as_view(), name='export'),
    url(r'^sources/create/$', sources.Form.as_view(), name='sources_create'),
    url(r'^sources/json/$', sources.SourceJsonListView.as_view(),
        name='source_json_list'),
    url(r'^sources/delete_rows/$', sources.SourceDeleteRowsView.as_view(),
        name='source_delete_rows'),

    url(r'^api/(?P<path>.+)$', 'api_proxy.proxy_view', name='api_proxy'),
    url(r'^webservices/$', webservices.WebservicesView.as_view(),
        name='webservices'),
)
