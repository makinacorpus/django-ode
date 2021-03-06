# -*- encoding: utf-8 -*-
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render

from django_custom_datatables_view.base_datatable_view import BaseDatatableView
from frontend.api_client import APIClient


def data_list_to_dict(data_list):
    result = {}
    for data_field in data_list:
        key = data_field['name']
        result[key] = data_field['value']
    return result


class LoginRequiredMixin(object):
    """
    View mixin which requires that the user is authenticated.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class ProviderLoginRequiredMixin(object):
    """
    View mixin which requires that the user is authenticated AND is a provider
    """
    @staticmethod
    def access_allowed(user):
        return user.is_superuser or user.organization.is_provider

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        if self.access_allowed(request.user):
            return super(ProviderLoginRequiredMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class APIFormView(LoginRequiredMixin, View):

    def __init__(self, *args, **kwargs):
        super(APIFormView, self).__init__(*args, **kwargs)
        self.api = APIClient(self.endpoint)

    def _update_context_data(self, context=None):

        if context is None:
            context = {}

        defined_context = self.get_context()
        new_context = dict(list(context.items()) +
                           list(defined_context.items()))

        return new_context

    def error_list_to_dict(self, api_errors):
        """
        Convert error list returned by the API into a dictionary
        of error messages indexed by field names.
        """
        result = {}
        for error in api_errors:
            name = error['name']
            if '.' in name:
                # Error names returned by the API look like
                # items.<error_index>.data.<field_name>
                field_name = name.split('.')[3]
            else:
                field_name = name
            if field_name == 'videos':
                field_name = 'media_video'
            elif field_name == 'sounds':
                field_name = 'media_audio'
            elif field_name == 'images':
                num = int(name.split('.')[4])
                if num == 0:
                    field_name = 'media_photo'
                elif num == 1:
                    field_name = 'media_photo2'
            result[field_name] = error['description']
        return result

    def get_context(self):
        return {}

    def prepare_api_input(self, dict_data):

        formatted_data = []
        for key, value in dict_data.items():
            if key in ('categories', 'tags'):
                value = [part.strip() for part in value.split(',')]
                value = list(filter(None, value))
            formatted_data.append(
                {'name': key, 'value': value}
            )

        post_data = {
            'template': {
                'data': formatted_data
            }
        }

        return post_data

    def get_response_data(self, data):
        return self.api.post(data, self.request.user.id)

    def error(self, request, user_input, response_data, do_render=True,
              object_id=None):
        context = dict(response_data)
        context['input'] = user_input
        context['errors'] = self.error_list_to_dict(response_data['errors'])
        context['object_id'] = object_id
        messages.error(request, self.error_message, extra_tags='danger')
        if 'items' in context['errors'].keys():
            messages.error(request, context['errors']['items'],
                           extra_tags='danger')
        new_context = self._update_context_data(context)
        if do_render:
            return render(request, self.template_name, new_context)

    def success(self, request, response_data, do_render=True, object_id=None):
        new_context = self._update_context_data()
        new_context['object_id'] = object_id
        messages.success(request, self.success_message)
        if do_render:
            return render(request, self.template_name, new_context)

    def post(self, request, *args, **kwargs):

        user_input = request.POST.dict()
        user_input.pop('csrfmiddlewaretoken', None)
        api_input = dict(user_input)

        post_data = self.prepare_api_input(api_input)
        object_id = kwargs.get('id')
        if object_id:
            response_data = self.api.put(object_id, post_data,
                                         self.request.user.id)
        else:
            response_data = self.get_response_data(post_data)

        if (isinstance(response_data, dict)
                and response_data.get('status') == 'error'):
            return self.error(request, user_input, response_data,
                              object_id=object_id)
        else:
            return self.success(request, response_data, object_id=object_id)

    def prepare_fields_content(self, data_list):
        return data_list_to_dict(data_list)

    def get(self, request, *args, **kwargs):
        object_context = None
        object_id = kwargs.get('id')
        if object_id:
            api = APIClient(self.endpoint)
            response = api.get(self.request.user.id, object_id=object_id)
            if response.get('status') == 404:
                return HttpResponseNotFound(
                    _(u"Auncun évément trouvé pour cet id"))

            item = response['collection']['items'][0]
            object_context = {
                'input': self.prepare_fields_content(item['data']),
                'object_id': object_id,
            }
        new_context = self._update_context_data(object_context)
        return render(self.request, self.template_name, new_context)


class APIDatatableBaseView(BaseDatatableView):

    endpoint = None
    api_columns = None

    def get_sort_by(self):
        raise NotImplementedError()

    def get_xpath_ind(self, xpath_value):

        try:
            ind = int(xpath_value)
        except ValueError:
            ind = xpath_value

        return ind

    def get_data_from_field(self, data, field, default=''):
        data = data_list_to_dict(data)

        xpath = field.split(".")

        xelement = self.get_xpath_ind(xpath[0])

        if len(xpath) == 1:
            if xelement in data:
                return data[xelement]
            else:
                return default
        else:
            return self.get_data_from_field(
                data[xelement],
                ".".join(xpath[1:]))

    def get_index_for(self, field_name):

        for i, column in enumerate(self.api_columns):

            column_splitted = column.split(".")
            if len(column_splitted) > 1:
                field_to_compare = column_splitted[-1]
            else:
                field_to_compare = column_splitted[0]

            if field_to_compare == field_name:
                return i

        return None

    def get_sort_direction(self):

        s_sort_dir = self.request.REQUEST.get('sSortDir_0', 'desc')

        return s_sort_dir

    def get_limit_value(self):

        limit = min(int(self.request.REQUEST.get('iDisplayLength', 10)),
                    self.max_display_length)

        return limit

    def get_offset_value(self):

        offset = int(self.request.REQUEST.get('iDisplayStart', 0))

        return offset

    def get_api_values(self, **kwargs):

        # Call distant API to get corresponding data
        api = APIClient(self.endpoint)
        response_data = api.get(self.request.user.id, **kwargs)

        return response_data

    def convert_api_to_datatable_data(self, api_data):

        converted_data = []
        collection = api_data['collection']

        for source in collection['items']:

            data = source['data']

            raw_data = []
            for field in self.api_columns:
                raw_value = self.get_data_from_field(data, field)
                raw_data.append(raw_value)

            converted_data.append(raw_data)

        return converted_data

    def total_records(self, api_data):
        return api_data['collection']['total_count']

    def returned_records(self, api_data):
        return api_data['collection']['total_count']

    def prepare_results(self, api_data):
        return api_data

    def get_context_data(self, *args, **kwargs):

        sort_by = self.get_sort_by()
        sort_direction = self.get_sort_direction()
        limit = self.get_limit_value()
        offset = self.get_offset_value()

        get_args = dict(sort_by=sort_by,
                        limit=limit,
                        offset=offset,
                        sort_direction=sort_direction)
        response_data = self.get_api_values(**get_args)

        api_data = self.convert_api_to_datatable_data(response_data)

        aaData = self.prepare_results(api_data)

        ret = {'sEcho': int(self.request.REQUEST.get('sEcho', 0)),
               'iTotalRecords': self.total_records(response_data),
               'iTotalDisplayRecords': self.returned_records(response_data),
               'aaData': aaData
               }

        return ret
