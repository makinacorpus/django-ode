# -*- encoding: utf-8 -*-
import isodate

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View

from frontend.views.base import (APIForm,
                                 LoginRequiredMixin,
                                 APIDatatableBaseView)
from frontend.api_client import APIClient


class EventListingFieldsMixin(object):

    column_labels = ['Title', 'Description', 'Start Date', 'End Date']
    # These fields are ODE API fields returned for each source record
    api_columns = ['title', 'description', 'start_time', 'end_time']

    endpoint = settings.EVENTS_ENDPOINT


class EventListingUserFieldsMixin(EventListingFieldsMixin):

    column_labels = ['Title', 'Description', 'Start Date', 'End Date',
                     'Suppression']
    # These fields are ODE API fields returned for each source record
    api_columns = ['title', 'description', 'start_time', 'end_time',
                   'id']


class Form(APIForm):

    template_name = 'event_form.html'
    list_template_name = 'event_list.html'
    endpoint = settings.EVENTS_ENDPOINT
    success_message = u"L'événement a été enregistré avec succès"
    error_message = u"L'événement n'a pas pu être enregistré"

    def add_context(self, *args, **kwargs):
        context = {}
        context['organization'] = self.request.user.organization
        return context

    def prepare_media(self, api_input):

        if 'media_photo' in api_input.keys() and api_input['media_photo']:
            image = {
                'url': api_input['media_photo'],
                'license': api_input['media_photo_license']
                }
            del api_input['media_photo']
            del api_input['media_photo_license']
            api_input['images'] = [image]
        if 'media_photo2' in api_input.keys() and api_input['media_photo2']:
            image = {
                'url': api_input['media_photo2'],
                'license': api_input['media_photo_license2']
                }
            del api_input['media_photo2']
            del api_input['media_photo_license2']
            if 'images' in api_input.keys():
                api_input['images'].append(image)
            else:
                api_input['images'] = [image]
        if 'media_video' in api_input.keys() and api_input['media_video']:
            video = {
                'url': api_input['media_video'],
                'license': api_input['media_video_license']
                }
            del api_input['media_video']
            del api_input['media_video_license']
            api_input['videos'] = [video]

        if 'media_audio' in api_input.keys() and api_input['media_audio']:
            sound = {
                'url': api_input['media_audio'],
                'license': api_input['media_audio_license']
                }
            del api_input['media_audio']
            del api_input['media_audio_license']
            api_input['sounds'] = [sound]
        return api_input

    def prepare_api_input(self, dict_data):

        dict_data = self.prepare_media(dict_data)
        user = self.request.user
        default_data = [
            {'name': 'firstname', 'value': user.first_name},
            {'name': 'lastname', 'value': user.last_name},
            {'name': 'email', 'value': user.email},
            {'name': 'telephone', 'value': user.phone_number},
            {'name': 'language', 'value': 'fr'},
            {'name': 'organiser', 'value': user.organization.name},
            ]
        formatted_data = super(Form, self)\
            .prepare_api_input(dict_data)
        formatted_data.update(default_data)
        return formatted_data


class EventListView(EventListingFieldsMixin, LoginRequiredMixin, TemplateView):
    template_name = 'event_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EventListView, self).get_context_data(*args, **kwargs)

        context['event_column_labels'] = self.column_labels
        context['user_only'] = False
        return context


class EventListUserView(EventListingUserFieldsMixin, EventListView):

    def get_context_data(self, *args, **kwargs):
        context = super(EventListUserView, self).\
            get_context_data(*args, **kwargs)

        context['user_only'] = True
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


class EventJsonListUserView(EventListingUserFieldsMixin, EventJsonListView):

    def prepare_results(self, api_data):
        api_data = super(EventJsonListUserView, self).prepare_results(api_data)
        delete_index = self.get_index_from_column_label('Suppression')
        for data in api_data:
            for i, field in enumerate(data):
                if i == delete_index:
                    raw_data = data[i]
                    data[i] = '<input type="checkbox"'
                    data[i] += ' class="datatable-delete"'
                    data[i] += ' data-id="' + str(raw_data) + '"'
                    data[i] += '>'
        return api_data

    def get_api_values(self, **kwargs):
        kwargs.setdefault('provider_id', self.request.user.id)
        return super(EventJsonListUserView, self).get_api_values(**kwargs)


class EventsDeleteRowsView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        ids_to_delete = request.POST.getlist('id_to_delete')

        self.api = APIClient(settings.EVENTS_ENDPOINT)
        for id_to_delete in ids_to_delete:
            response = self.api.delete(id_to_delete, request.user.id)
            # If there is a problem when deleting a resource,
            # we raise an exception to warn user that there is "a" problem
            no_content = 204
            if response.status_code != no_content:
                return HttpResponseServerError()

        return HttpResponse("Done")
