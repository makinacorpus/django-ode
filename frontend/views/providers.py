# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, DetailView

from django_custom_datatables_view.base_datatable_view import BaseDatatableView

from accounts.models import Organization
from .base import LoginRequiredMixin


class ProviderListView(LoginRequiredMixin, TemplateView):
    template_name = 'provider_list.html'
    column_labels = [_(u'Nom'), _(u"Type"),
                     _(u"Activité"), _(u"Ville")]

    def get_context_data(self, *args, **kwargs):

        context = super(ProviderListView, self).get_context_data(
            *args, **kwargs)
        context['column_labels'] = self.column_labels

        return context


class ProviderJsonListView(LoginRequiredMixin, BaseDatatableView):
    model = Organization
    columns = ['name', 'type', 'activity_field', 'town']
    order_columns = ['name', 'type', 'activity_field', 'town']

    def get_initial_queryset(self):

        return self.model.objects.filter(is_provider=True).all()

    def render_column(self, row, column):

        text = super(ProviderJsonListView, self).render_column(row, column)
        if column == 'name':
            text = (u'<a data-toggle="modal" '
                    u'data-target="#provider-modal" '
                    u'href="/provider/{}/">{}</a>'
                    .format(row.pk, text))
        return text


class ProviderView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'provider.html'
    context_object_name = 'organization'
