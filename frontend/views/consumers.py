# -*- encoding: utf-8 -*-
import csv
from StringIO import StringIO

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, DetailView, View

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


class ConsumerExportView(LoginRequiredMixin, View):
    fieldnames = ['name', 'activity_field', 'type', 'address', 'post_code',
                  'town', 'url', 'is_media', 'media_url', 'is_website',
                  'website_url', 'is_mobile_app', 'mobile_app_name',
                  'is_other', 'other_details']

    def get_consumer_data(self, consumer):
        data = {}
        for fieldname in self.fieldnames:
            data[fieldname] = getattr(consumer, fieldname)
        return data

    def get_csv_from_data(self, consumers):
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=self.fieldnames)
        writer.writeheader()
        for consumer in consumers:
            writer.writerow(self.get_consumer_data(consumer))
        return output.getvalue()

    def get(self, *args, **kwargs):
        consumers = Organization.objects.filter(is_consumer=True)
        response_csv = self.get_csv_from_data(consumers)
        response = HttpResponse(response_csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=events.csv'
        return response


class ConsumerJsonListView(LoginRequiredMixin, BaseDatatableView):
    model = Organization
    columns = ['name', 'type', 'activity_field', 'town']
    order_columns = ['name', 'type', 'activity_field', 'town']

    def get_initial_queryset(self):

        return self.model.objects.filter(is_consumer=True).all()

    def render_column(self, row, column):

        text = super(ConsumerJsonListView, self).render_column(row, column)
        if column == 'name':
            text = (u'<a data-toggle="modal" '
                    u'data-target="#consumer-modal" '
                    u'href="/consumer/{}/">{}</a>'
                    .format(row.pk, text))
        return text


class ConsumerView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'consumer.html'
    context_object_name = 'organization'
