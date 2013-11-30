# -*- encoding: utf-8 -*-

from django.conf import settings

from frontend.views.base import ProviderLoginRequiredMixin, APIForm
from frontend.views.sources import SourceListingFieldsMixin


class ImportView(ProviderLoginRequiredMixin,
                 SourceListingFieldsMixin,
                 APIForm):
    template_name = 'import.html'
    endpoint = settings.SOURCES_ENDPOINT
    resource_name_plural = 'sources'
    success_message = (u"Cette nouvelle source de données a été "
                       u"enregistrée avec succès")
    error_message = u"Cette source de données n'a pas pu être enregistrée"

    def add_context(self):
        context = dict(source_column_labels=self.column_labels)

        return context
