# -*- encoding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from django_custom_datatables_view.base_datatable_view import BaseDatatableView

from accounts.models import Organization
from .base import LoginRequiredMixin


class ConsumerListView(LoginRequiredMixin, TemplateView):
    template_name = 'consumer_list.html'
    column_labels = [_(u'Nom'), _(u"Type"),
                     _(u"Activité"), _(u"Ville")]

    def get_context_data(self, *args, **kwargs):

        context = super(ConsumerListView, self).get_context_data(
            *args, **kwargs)
        context['column_labels'] = self.column_labels

        return context


class ConsumerJsonListView(LoginRequiredMixin, BaseDatatableView):
    model = Organization
    columns = ['name', 'type', 'activity_field', 'town']
    order_columns = ['name', 'type', 'activity_field', 'town']

    def get_initial_queryset(self):

        return self.model.objects.filter(is_consumer=True).all()
