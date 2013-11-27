# -*- encoding: utf-8 -*-
from django.views.generic import TemplateView

from frontend.views.base import ProviderLoginRequiredMixin


class ImportView(ProviderLoginRequiredMixin, TemplateView):
    template_name = 'import.html'
    column_labels = ['ID', 'URL']

    def get_context_data(self, *args, **kwargs):

        context = super(ImportView, self).get_context_data(
            *args, **kwargs)
        context['column_labels'] = self.column_labels

        return context
