import requests
import json

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render


class APIForm(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(APIForm, self).dispatch(*args, **kwargs)

    def prepare_api_input(self, data):
        pass

    def post_to_api(self, data):
        response = requests.post(
            self.endpoint,
            data=json.dumps(data),
            headers={
                'X-ODE-Producer-Id': self.request.user.id,
                'Content-Type': 'application/json',
            })
        return response.json()

    def post(self, request):
        user_input = request.POST.dict()
        user_input.pop('csrfmiddlewaretoken', None)
        api_input = dict(user_input)
        self.prepare_api_input(api_input)
        post_data = {
            self.resource_name_plural: [api_input]
        }
        response_data = self.post_to_api(post_data)
        if response_data.get('status') == 'error':
            context = dict(response_data)
            context['input'] = user_input
            messages.error(request, self.error_message)
            return render(request, self.template_name, context)
        else:
            messages.success(request, self.success_message)
            return render(request, 'source_list.html')

    def get(self, request):
        return render(self.request, self.template_name)
