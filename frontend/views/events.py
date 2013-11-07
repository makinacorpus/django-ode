# -*- encoding: utf-8 -*-
import json
import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages


def merge_datetime(data):
    for prefix in ('start', 'end'):
        time_key = prefix + '_time'
        date_key = prefix + '_date'
        data[time_key] = 'T'.join([data[date_key], data[time_key]])
        del data[date_key]


@login_required
def create(request):
    if request.method == 'POST':
        input_data = request.POST.dict()
        input_data.pop('csrfmiddlewaretoken', None)
        merge_datetime(input_data)
        post_data = {
            'events': [input_data]
        }
        requests.post(
            settings.EVENTS_ENDPOINT,
            data=json.dumps(post_data),
            headers={
                'X-ODE-Producer-Id': request.user.id,
                'Content-Type': 'application/json',
            })
        messages.success(request,
                         u"L'événement a été enregistré avec succès")
    return render(request, 'event_form.html')
