# -*- encoding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect

from frontend.views.base import ProviderLoginRequiredMixin, APIForm
from frontend.views.sources import SourceListingFieldsMixin


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
    endpoint = settings.SOURCES_ENDPOINT

    def error(self, request, user_input, response_data):
        APIForm.error(self, request, user_input, response_data, render=False)
        return redirect('imports')

    def success(self, request, response_data):
        APIForm.success(self, request, response_data, render=False)
        return redirect('imports')


class APIImportFileForm(APIImportMixinForm):
    success_message = (u"Le fichier a été importé avec succès")
    error_message = u"Ce fichier n'a pas pu être importé"


class APIImportSourceForm(APIImportMixinForm):
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"
