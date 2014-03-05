# -*- encoding: utf-8 -*-
import json
import logging

from django.conf import settings
from django.shortcuts import render, redirect
from django import forms

from frontend.views.base import ProviderLoginRequiredMixin, APIFormView
from frontend.views.sources import SourceListingFieldsMixin

logger = logging.getLogger(__name__)


class ImportView(ProviderLoginRequiredMixin,
                 SourceListingFieldsMixin,
                 APIFormView):
    template_name = 'import.html'

    def get_context(self):
        return {
            'source_column_labels': self.column_labels,
        }

    def get(self, request, *args, **kwargs):
        new_context = self.get_context()
        return render(self.request, self.template_name, new_context)

    def success(self, request, response_data, **kwargs):
        APIFormView.success(self, request, response_data, do_render=False)
        return redirect('imports')


class ImportFileForm(forms.Form):
    events_file = forms.FileField(required=True)


class ImportFileView(ImportView):
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

    def _is_json(self, data):
        try:
            json.loads(data)
            return True
        except:
            return False

    def post(self, request, *args, **kwargs):
        form = ImportFileForm(request.POST, request.FILES)
        if not form.is_valid():
            context = self.get_context()
            context['errors'] = form.errors
            return render(request, self.template_name, context)
        data_file = form.cleaned_data['events_file']
        mimetype = data_file.content_type
        data = data_file.read()

        if self._is_json(data):
            data = data.decode('utf-8')
            response_data = self._post_json(json.loads(data))
        else:
            response_data = self.api.post(data, self.request.user.id,
                                          mimetype=mimetype)
        if (isinstance(response_data, dict)
                and response_data.get('status') == 'error'):
            return self.error(request, {}, response_data)
        else:
            return self.success(request, response_data)


class ImportSourceView(ImportView):
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"
    endpoint = settings.SOURCES_ENDPOINT
