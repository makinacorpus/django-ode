# -*- encoding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from frontend.views.base import (APIForm,
                                 LoginRequiredMixin,
                                 APIDatatableBaseView)
from frontend.api_client import APIClient


class SourceListingFieldsMixin(object):

    source_column_labels = ['URL']
    # These fields are ODE API fields returned for each source record
    source_api_columns = ['url']

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

        return self.source_api_columns[i_sort_col]
