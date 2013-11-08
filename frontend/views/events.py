# -*- encoding: utf-8 -*-
from django.conf import settings

from frontend.views.base import APIForm


def merge_datetime(data):
    for prefix in ('start', 'end'):
        time_key = prefix + '_time'
        date_key = prefix + '_date'
        data[time_key] = 'T'.join([data[date_key], data[time_key]])
        del data[date_key]


class Form(APIForm):

    template_name = 'event_form.html'
    endpoint = settings.EVENTS_ENDPOINT
    success_message = u"L'événement a été enregistré avec succès"
    resource_name_plural = 'events'

    def prepare_api_input(self, data):
        merge_datetime(data)
