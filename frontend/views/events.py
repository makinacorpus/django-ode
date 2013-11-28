# -*- encoding: utf-8 -*-
from django.conf import settings
from django.views.generic import TemplateView

from frontend.views.base import (APIForm,
                                 LoginRequiredMixin,
                                 APIDatatableBaseView)


class EventListingFieldsMixin(object):

    event_column_labels = ['Title', 'Uid']
    # These fields are ODE API fields returned for each source record
    api_columns = ['title', 'uid']

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

        context['event_column_labels'] = self.event_column_labels
        print('HEY')
        return context


class EventJsonListView(EventListingFieldsMixin,
                        LoginRequiredMixin,
                        APIDatatableBaseView):

    def get_sort_by(self):

        i_sort_col = int(self.request.REQUEST.get('iSortCol_0', 0))

        return self.api_columns[i_sort_col]
