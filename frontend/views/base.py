from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.api_client import APIClient


def error_list_to_dict(api_errors):
    """
    Convert error list returned by the API into a dictionary of error messages
    indexed by field names.
    """
    result = {}
    for error in api_errors:
        name = error['name']
        # Error names returned by the API look like
        # <resource_name>.<error_index>.<field_name>
        field_name = name.split('.')[2]
        result[field_name] = error['description']
    return result


class APIForm(View):

    def __init__(self, *args, **kwargs):
        super(APIForm, self).__init__(*args, **kwargs)
        self.api = APIClient(self.endpoint)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(APIForm, self).dispatch(*args, **kwargs)

    def prepare_api_input(self, data):
        pass

    def post(self, request):
        user_input = request.POST.dict()
        user_input.pop('csrfmiddlewaretoken', None)
        api_input = dict(user_input)
        self.prepare_api_input(api_input)
        post_data = {
            self.resource_name_plural: [api_input]
        }
        response_data = self.api.post(post_data, self.request.user.id)
        if response_data.get('status') == 'error':
            context = dict(response_data)
            context['input'] = user_input
            context['errors'] = error_list_to_dict(response_data['errors'])
            messages.error(request, self.error_message, extra_tags='danger')
            return render(request, self.template_name, context)
        else:
            messages.success(request, self.success_message)
            return redirect(self.resource_name_plural + '_list')

    def get(self, request):
        return render(self.request, self.template_name)
