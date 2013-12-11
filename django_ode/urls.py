from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'django_ode.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'', include('frontend.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
