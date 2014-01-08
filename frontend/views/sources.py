# -*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from django.views.generic import View

from frontend.views.base import (APIFormView,
                                 LoginRequiredMixin,
                                 APIDatatableBaseView)
from frontend.api_client import APIClient


class SourceListingFieldsMixin(object):

    column_labels = ['URL', 'Suppression']
    # These fields are ODE API fields returned for each source record
    api_columns = ['url', 'id']

    endpoint = settings.SOURCES_ENDPOINT


class Form(SourceListingFieldsMixin, APIFormView):
    template_name = 'import.html'
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"


class SourceJsonListView(SourceListingFieldsMixin,
                         LoginRequiredMixin,
                         APIDatatableBaseView):

    def get_sort_by(self):

        i_sort_col = int(self.request.REQUEST.get('iSortCol_0', 0))

        return self.api_columns[i_sort_col]

    def prepare_results(self, api_data):

        delete_index = self.get_index_for('id')

        for data in api_data:

            for i, field in enumerate(data):
                if i == delete_index:
                    raw_data = data[i]
                    data[i] = '<input type="checkbox"'
                    data[i] += ' class="datatable-delete"'
                    data[i] += ' data-id="' + str(raw_data) + '"'
                    data[i] += '>'

        return api_data


class SourceDeleteRowsView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        ids_to_delete = request.POST.getlist('ids')

        self.api = APIClient(settings.SOURCES_ENDPOINT)
        for id_to_delete in ids_to_delete:
            response = self.api.delete(id_to_delete, request.user.id)
            # If there is a problem when deleting a resource,
            # we raise an exception to warn user that there is "a" problem
            no_content = 204
            if response.status_code != no_content:
                return HttpResponseServerError()

        return HttpResponse("Done")
