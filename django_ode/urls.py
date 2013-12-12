from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^blog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'', include('frontend.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(
    'django.contrib.flatpages.views',
    (r'^(?P<url>.*/)$', 'flatpage'),
)
