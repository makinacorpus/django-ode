# -*- encoding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from frontend.views.base import APIForm
from frontend.api_client import APIClient


class Form(APIForm):

    template_name = 'event_form.html'
    list_template_name = 'event_list.html'
    endpoint = settings.EVENTS_ENDPOINT
    success_message = u"L'événement a été enregistré avec succès"
    error_message = u"L'événement n'a pas pu être enregistré"
    resource_name_plural = 'events'


@login_required
def list(request):
    api = APIClient(settings.EVENTS_ENDPOINT)
    response_data = api.get(request.user.id)
    return render(request, 'event_list.html', response_data)
