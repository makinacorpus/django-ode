# -*- encoding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from frontend.views.base import APIForm
from frontend.api_client import APIClient


class Form(APIForm):
    template_name = 'source_form.html'
    list_template_name = 'source_list.html'
    endpoint = settings.SOURCES_ENDPOINT
    resource_name_plural = 'sources'
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"


@login_required
def list(request):
    api = APIClient(settings.SOURCES_ENDPOINT)
    response_data = api.get(request.user.id)
    return render(request, 'source_list.html', response_data)
