# -*- encoding: utf-8 -*-
import isodate
import six

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _, ugettext
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect

from accounts.models import User
from frontend.views.base import (APIForm,
                                 LoginRequiredMixin,
                                 ProviderLoginRequiredMixin,
                                 APIDatatableBaseView,
                                 data_list_to_dict)
from frontend.api_client import APIClient
from frontend import html


def convert_iso_to_listing_date(iso_date):
    # API format for date is "2012-01-16T19:00:00"
    # Result would be "Le 16/01/2012 à 19h00"
    dt = isodate.parse_datetime(iso_date)
    format_string = ugettext(u"Le %d/%m/%Y à %Hh%M")
    if six.PY2:
        format_string = format_string.encode('utf-8')
    return dt.strftime(format_string)


class EventView(LoginRequiredMixin, View):

    date_columns = ['start_time', 'end_time', 'publication_start',
                    'publication_end']

    def prepare_data(self, event_data):
        event_data = data_list_to_dict(event_data)
        for key, value in event_data.items():
            if key in self.date_columns:
                event_data[key] = convert_iso_to_listing_date(value)
        return event_data

    def get(self, request, *args, **kwargs):
        api = APIClient(settings.EVENTS_ENDPOINT)
        event_id = kwargs.get('id')
        response = api.get(request.user.id, object_id=event_id)
        if 'errors' in response.keys() and response['status'] == 404:
            return render(request, 'event_not_found.html')
        event_data = response['collection']['items'][0]['data']
        context = {'event': self.prepare_data(event_data)}
        return render(request, 'event.html', context)


class EventListingFieldsMixin(object):

    column_labels = [_(u'Titre'), _(u'Début'), _(u'Fin'), _(u'Structure')]
    # These fields are ODE API fields returned for each source record
    api_columns = ['title', 'start_time', 'end_time', 'provider_id', 'id']

    endpoint = settings.EVENTS_ENDPOINT


class EventListingUserFieldsMixin(EventListingFieldsMixin):

    column_labels = [_(u'Titre'), _(u'Début'), _(u'Fin'), _(u'Publication'),
                     _(u'Expiration'), _(u'Suppression'), _(u'Duplication')]
    # These fields are ODE API fields returned for each source record
    api_columns = ['title', 'start_time', 'end_time', 'publication_start',
                   'publication_end', 'id', 'id']


class Form(APIForm):

    template_name = 'event_form.html'
    list_template_name = 'event_list.html'
    endpoint = settings.EVENTS_ENDPOINT
    success_message = _(u"L'événement a été enregistré avec succès")
    error_message = _(u"L'événement n'a pas pu être enregistré")

    def add_context(self, *args, **kwargs):
        context = {}
        context['organization'] = self.request.user.organization
        return context

    def _add_media(self, url_key, license_key, medias_name, api_input):
        media = {
            'url': api_input[url_key],
            'license': api_input[license_key]
            }
        del api_input[url_key]
        del api_input[license_key]
        if medias_name in api_input.keys():
            api_input[medias_name].append(media)
        else:
            api_input[medias_name] = [media]
        return api_input

    def prepare_media(self, api_input):

        if 'media_photo' in api_input.keys() and api_input['media_photo']:
            api_input = self._add_media('media_photo', 'media_photo_license',
                                        'images', api_input)
        if 'media_photo2' in api_input.keys() and api_input['media_photo2']:
            api_input = self._add_media('media_photo2', 'media_photo_license2',
                                        'images', api_input)
        if 'media_video' in api_input.keys() and api_input['media_video']:
            api_input = self._add_media('media_video', 'media_video_license',
                                        'videos', api_input)
        if 'media_audio' in api_input.keys() and api_input['media_audio']:
            api_input = self._add_media('media_audio', 'media_audio_license',
                                        'sounds', api_input)
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
        formatted_data['template']['data'] += default_data
        return formatted_data

    def format_daterange(self, start_time, end_time):
        start_datetime = isodate.parse_datetime(start_time)
        end_datetime = isodate.parse_datetime(end_time)
        date_format = u'%d/%m/%Y %H:%M'
        return u' - '.join([start_datetime.strftime(date_format),
                            end_datetime.strftime(date_format)])

    @staticmethod
    def has_publication_dates(data_dict):
        return ('publication_start' in data_dict
                and 'publication_end' in data_dict)

    def prepare_fields_media(self, data_dict):
        if 'images' in data_dict.keys():
            data_dict['media_photo'] = data_dict['images'][0]['url']
            data_dict['media_photo_license'] = \
                data_dict['images'][0]['license']
            if len(data_dict['images']) >= 2:
                data_dict['media_photo2'] = data_dict['images'][1]['url']
                data_dict['media_photo_license2'] = \
                    data_dict['images'][1]['license']
        if 'videos' in data_dict.keys():
            data_dict['media_video'] = data_dict['videos'][0]['url']
            data_dict['media_video_license'] = \
                data_dict['videos'][0]['license']
        if 'sounds' in data_dict.keys():
            data_dict['media_audio'] = data_dict['sounds'][0]['url']
            data_dict['media_audio_license'] = \
                data_dict['sounds'][0]['license']
        return data_dict

    def prepare_fields_content(self, data_list):
        data_dict = data_list_to_dict(data_list)
        for key in ('tags', 'categories'):
            data_dict[key] = u', '.join(data_dict[key])
        data_dict['daterange'] = self.format_daterange(
            data_dict['start_time'], data_dict['end_time'])
        if self.has_publication_dates(data_dict):
            data_dict['daterange_publication'] = self.format_daterange(
                data_dict['publication_start'], data_dict['publication_end'])
        data_dict = self.prepare_fields_media(data_dict)
        return data_dict

    def success(self, request, response_data, do_render=False, object_id=None):
        super(Form, self).success(request, response_data, do_render=False,
                                  object_id=object_id)
        return redirect('event_list_user')


class EventListView(EventListingFieldsMixin, LoginRequiredMixin, TemplateView):
    template_name = 'event_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EventListView, self).get_context_data(*args, **kwargs)

        context['event_column_labels'] = self.column_labels
        context['user_only'] = False
        return context


class EventListUserView(EventListingUserFieldsMixin,
                        ProviderLoginRequiredMixin, EventListView):

    def get_context_data(self, *args, **kwargs):
        context = super(EventListUserView, self).\
            get_context_data(*args, **kwargs)

        context['user_only'] = True
        return context


class EventJsonListView(EventListingFieldsMixin,
                        LoginRequiredMixin,
                        APIDatatableBaseView):

    date_columns = ['start_time', 'end_time']

    def get_sort_by(self):

        i_sort_col = int(self.request.REQUEST.get('iSortCol_0', 0))

        return self.api_columns[i_sort_col]

    def _getOrganizationFromProviderId(self, provider_id):
        try:
            user = User.objects.get(pk=provider_id)
        except ValueError:
            # id is a string. Only integer allowed.
            return ''
        except User.DoesNotExist:
            return ''
        organization = user.organization
        text = (u'<a data-toggle="modal" '
                u'data-target="#events-modal" '
                u'href="/provider/{}/">{}</a>'
                .format(organization.pk, organization.name))
        return text

    def _getTitle(self, title, event_id):
        url = reverse('event', args=[event_id])
        return html.modal_link('events', url, title)

    def prepare_results(self, api_data):

        indexes = []
        for date_column in self.date_columns:
            indexes.append(self.get_index_for(date_column))
        provider_column_index = self.get_index_for('provider_id')
        title_column_index = self.get_index_for('title')
        event_id_column_index = self.get_index_for('id')
        for data in api_data:
            for i, field_value in enumerate(data):
                if i in indexes and data[i]:
                    data[i] = convert_iso_to_listing_date(data[i])
                elif i == provider_column_index:
                    data[i] = self._getOrganizationFromProviderId(data[i])
                elif i == title_column_index:
                    data[i] = self._getTitle(data[i],
                                             data[event_id_column_index])
        return api_data


class EventJsonListUserView(EventListingUserFieldsMixin, EventJsonListView):

    date_columns = ['start_time', 'end_time', 'publication_start',
                    'publication_end']

    def _getTitle(self, title, event_id):
        url = reverse('event_edit', args=[event_id])
        return html.link(url, title)

    def prepare_results(self, api_data):
        api_data = super(EventJsonListUserView, self).prepare_results(api_data)
        delete_index = self.get_index_for('id')
        duplicate_index = delete_index + 1
        for data in api_data:
            for i, field in enumerate(data):
                raw_data = data[i]
                if i == delete_index:
                    data[i] = html.checkbox('datatable-delete', raw_data)
                elif i == duplicate_index:
                    data[i] = html.checkbox('datatable-duplicate', raw_data)
        return api_data

    def get_api_values(self, **kwargs):
        kwargs.setdefault('provider_id', self.request.user.id)
        return super(EventJsonListUserView, self).get_api_values(**kwargs)


class EventsDeleteRowsView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        ids_to_delete = request.POST.getlist('ids')

        self.api = APIClient(settings.EVENTS_ENDPOINT)
        for id_to_delete in ids_to_delete:
            response = self.api.delete(id_to_delete, request.user.id)
            # If there is a problem when deleting a resource,
            # we raise an exception to warn user that there is "a" problem
            no_content = 204
            if response.status_code != no_content:
                return HttpResponseServerError()

        return HttpResponse("Done")


class EventsDuplicateRowsView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        event_ids = request.POST.getlist('ids')

        self.api = APIClient(settings.EVENTS_ENDPOINT)
        for event_id in event_ids:
            response = self.api.get(request.user.id, object_id=event_id)
            event_data = response['collection']['items'][0]['data']
            event_data = [field for field in event_data
                          if field['name'] != 'id']
            post_data = {'template': {'data': event_data}}
            response = self.api.post(post_data, request.user.id)
        return HttpResponse("Done")
