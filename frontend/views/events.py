# -*- encoding: utf-8 -*-
import isodate

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from frontend.views.base import (APIForm,
                                 LoginRequiredMixin,
                                 APIDatatableBaseView)


class EventListingFieldsMixin(object):

    column_labels = ['Title', 'Description', 'Start Date', 'End Date']
    # These fields are ODE API fields returned for each source record
    api_columns = ['title', 'description', 'start_time', 'end_time']

    endpoint = settings.EVENTS_ENDPOINT


class Form(APIForm):

    template_name = 'event_form.html'
    list_template_name = 'event_list.html'
    endpoint = settings.EVENTS_ENDPOINT
    success_message = u"L'événement a été enregistré avec succès"
    error_message = u"L'événement n'a pas pu être enregistré"
    resource_name_plural = 'events'


class EventListView(EventListingFieldsMixin, LoginRequiredMixin, TemplateView):
    template_name = 'event_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EventListView, self).get_context_data(*args, **kwargs)

        context['event_column_labels'] = self.column_labels
        return context


def convert_iso_to_listing_date(iso_date):
    # API format for date is "2012-01-16T19:00:00"
    # Result would be "Le 16/01/2012 à 19h00"
    dt = isodate.parse_datetime(iso_date)
    datatable_date = _(u"Le {dd}/{MM}/{yyyy} à {hh}h{mm}").format(
        dd=str(dt.day).rjust(2, '0'),
        MM=str(dt.month).rjust(2, '0'),
        yyyy=dt.year,
        hh=str(dt.hour).rjust(2, '0'),
        mm=str(dt.minute).rjust(2, '0'))

    return datatable_date


class EventJsonListView(EventListingFieldsMixin,
                        LoginRequiredMixin,
                        APIDatatableBaseView):

    def get_sort_by(self):

        i_sort_col = int(self.request.REQUEST.get('iSortCol_0', 0))

        return self.api_columns[i_sort_col]

    def prepare_results(self, api_data):

        start_time_index = self.get_index_for('start_time')
        end_time_index = self.get_index_for('end_time')

        for data in api_data:

            for i, field_value in enumerate(data):

                if i == start_time_index or i == end_time_index:

                    data[i] = convert_iso_to_listing_date(data[i])

        return api_data
