# -*- encoding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from frontend.views.base import (APIForm,
                                 LoginRequiredMixin,
                                 APIDatatableBaseView)
from frontend.api_client import APIClient


class Form(APIForm):
    template_name = 'source_form.html'
    list_template_name = 'source_list.html'
    endpoint = settings.SOURCES_ENDPOINT
    resource_name_plural = 'sources'
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"


class SourceListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        api = APIClient(settings.SOURCES_ENDPOINT)
        response_data = api.get(request.user.id)
        return render(request, 'source_list.html', response_data)


class SourceJsonListView(LoginRequiredMixin, APIDatatableBaseView):
    # These fields are ODE API fields returned for each source record
    columns = ['id', 'url']

    # TODO : remove this function when parameter total_count is returned by api
    def total_records(self, api_data):

        return len(api_data['sources'])

    def returned_records(self, api_data):

        return len(api_data['sources'])

    def prepare_results(self, api_data):

        displayed_data = []
        sources = api_data['sources']

        for source in sources:

            raw_data = []
            for field in self.columns:
                raw_data.append(source[field])

            displayed_data.append(raw_data)

        return displayed_data
