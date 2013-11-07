# -*- encoding: utf-8 -*-
import requests
import json

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def create(request):
    if request.method == 'POST':
        source_data = request.POST.dict()
        source_data.pop('csrfmiddlewaretoken', None)
        post_data = {
            'sources': [source_data]
        }
        response = requests.post(
            settings.SOURCES_ENDPOINT,
            data=json.dumps(post_data),
            headers={
                'X-ODE-Producer-Id': request.user.id,
                'Content-Type': 'application/json',
            })
        response_data = response.json()
        if response_data.get('status') == 'error':
            context = dict(response_data)
            context['input'] = source_data
            messages.error(
                request,
                u"Cette source de données n'a pas pu être enregistrée")
            return render(request, 'source_form.html', context)
        else:
            messages.success(
                request,
                u"Cette nouvelle source de données a "
                + u"été enregistrée avec succès")
            return render(request, 'source_list.html')
    return render(request, 'source_form.html')


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
