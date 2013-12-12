from django.views.generic.base import View
from django.shortcuts import render
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token


class WebservicesView(View):

    def get(self, request):
        token = Token.objects.get(user=request.user)
        events_path = reverse('api_proxy', kwargs={'path': 'v1/events'})
        sources_path = reverse('api_proxy', kwargs={'path': 'v1/sources'})
        return render(request, 'webservices.html', {
            'key': token.key,
            'events_url': request.build_absolute_uri(events_path),
            'sources_url': request.build_absolute_uri(sources_path),
        })
