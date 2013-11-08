# -*- encoding: utf-8 -*-
import requests
import json

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from frontend.views.base import APIForm


class Form(APIForm):
    endpoint = settings.SOURCES_ENDPOINT
    resource_name_plural = 'sources'
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"


@login_required
def list(request):
    response = requests.get(
        settings.SOURCES_ENDPOINT,
        headers={
            'X-ODE-Producer-Id': request.user.id,
            'Accept': 'application/json',
        })
    response_data = response.json()
    return render(request, 'source_list.html', response_data)
