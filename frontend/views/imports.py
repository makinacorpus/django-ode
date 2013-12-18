# -*- encoding: utf-8 -*-
import json
import logging

from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect

from frontend.views.base import ProviderLoginRequiredMixin, APIForm
from frontend.views.sources import SourceListingFieldsMixin

logger = logging.getLogger(__name__)


class ImportView(ProviderLoginRequiredMixin,
                 SourceListingFieldsMixin,
                 View):
    template_name = 'import.html'

    def add_context(self):
        context = dict(source_column_labels=self.column_labels)
        return context

    def get(self, request, *args, **kwargs):
        new_context = self.add_context()
        return render(self.request, self.template_name, new_context)


class APIImportMixinForm(ImportView, APIForm):
    template_name = 'import.html'

    def success(self, request, response_data):
        APIForm.success(self, request, response_data, do_render=False)
        return redirect('imports')


class APIImportFileForm(APIImportMixinForm):
    success_message = (u"Le fichier a été importé avec succès")
    error_message = u"Ce fichier n'a pas pu être importé"
    endpoint = settings.EVENTS_ENDPOINT

    def _post_json(self, data):
        response_data = None
        for item in data.get('collection', {}).get('items', []):
            formatted_data = []
            for value in item['data']:
                formatted_data.append(value)
            post_data = {
                'template': {
                    'data': formatted_data
                    }
                }
            response_data = self.api.post(post_data, self.request.user.id)
            if (isinstance(response_data, dict)
                    and response_data.get('status') == 'error'):
                break
        return response_data

    def post(self, request, *args, **kwargs):
        data_file = self.request.FILES['events_file']
        mimetype = data_file.content_type
        data = data_file.read()
        if mimetype == 'application/json':
            response_data = self._post_json(json.loads(data))
        else:
            response_data = self.api.post(data, self.request.user.id,
                                          mimetype=mimetype)
        if (isinstance(response_data, dict)
                and response_data.get('status') == 'error'):
            return self.error(request, {}, response_data)
        else:
            return self.success(request, response_data)


class APIImportSourceForm(APIImportMixinForm):
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"
    endpoint = settings.SOURCES_ENDPOINT
