# -*- encoding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse

from frontend.views.base import APIForm


class ExportView(APIForm):
    template_name = 'export.html'
    endpoint = settings.EVENTS_ENDPOINT
    success_message = u"Événements exportés"
    error_message = u"Erreur lors de l'export"

    MIMETYPE_TO_EXT = {
        'application/vnd.collection+json': 'json',
        'text/csv': 'csv',
        'text/calendar': 'ics'
        }

    def prepare_api_input(self, dict_data):
        data = {
            'start_time': dict_data['start_time'],
            'end_time': dict_data['end_time'],
            'format': dict_data['format']
            }
        return data

    def get_response_data(self, data):
        if data['format'] == 'json':
            mimetype = 'application/vnd.collection+json'
        elif data['format'] == 'csv':
            mimetype = 'text/csv'
        elif data['format'] == 'ical':
            mimetype = 'text/calendar'
        self.mimetype = mimetype
        return self.api.get(self.request.user.id, mimetype=mimetype,
                            json=False, **data)

    def success(self, request, response_data, **kwargs):
        response = HttpResponse(response_data, content_type=self.mimetype)
        response['Content-Disposition'] = 'attachment; filename=events.%s'\
            % self.MIMETYPE_TO_EXT[self.mimetype]
        return response
