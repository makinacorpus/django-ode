# -*- encoding: utf-8 -*-

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from frontend.views.base import (APIForm,
                                 LoginRequiredMixin,
                                 APIDatatableBaseView)
from frontend.api_client import APIClient


class SourceListingFieldsMixin(object):

    column_labels = ['URL', 'Suppression']
    # These fields are ODE API fields returned for each source record
    api_columns = ['url', 'id']

    endpoint = settings.SOURCES_ENDPOINT


class Form(SourceListingFieldsMixin, APIForm):
    template_name = 'import.html'
    resource_name_plural = 'sources'
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"


class SourceListView(SourceListingFieldsMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        api = APIClient(self.endpoint)
        response_data = api.get(request.user.id)
        return render(request, 'source_list.html', response_data)


class SourceJsonListView(SourceListingFieldsMixin,
                         LoginRequiredMixin,
                         APIDatatableBaseView):

    def get_sort_by(self):

        i_sort_col = int(self.request.REQUEST.get('iSortCol_0', 0))

        return self.api_columns[i_sort_col]

    def prepare_results(self, api_data):

        delete_index = self.get_index_from_column_label('Suppression')

        for data in api_data:

            for i, field in enumerate(data):
                if i == delete_index:
                    raw_data = data[i]
                    data[i] = '<input type="checkbox"'
                    data[i] += ' class="datatable-delete"'
                    data[i] += ' data-id="' + str(raw_data) + '"'
                    data[i] += '>'

        return api_data


class SourceDeleteRowsView(View):

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            ids_to_delete = request.POST.getlist('id_to_delete')

            self.api = APIClient(settings.SOURCES_ENDPOINT)
            for id_to_delete in ids_to_delete:
                print(id_to_delete, request.user.id)
                response_data = self.api.delete(id_to_delete,
                                                request.user.id)
                print(response_data)
                #if response_data['status'] == 404:

            return HttpResponse("Done")

        return HttpResponse("Not the right way...")
