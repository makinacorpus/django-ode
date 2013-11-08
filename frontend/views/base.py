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

    def post(self, request):
        source_data = request.POST.dict()
        source_data.pop('csrfmiddlewaretoken', None)
        post_data = {
            self.resource_name_plural: [source_data]
        }
        response = requests.post(
            self.endpoint,
            data=json.dumps(post_data),
            headers={
                'X-ODE-Producer-Id': request.user.id,
                'Content-Type': 'application/json',
            })
        response_data = response.json()
        if response_data.get('status') == 'error':
            context = dict(response_data)
            context['input'] = source_data
            messages.error(request, self.error_message)
            return render(request, 'source_form.html', context)
        else:
            messages.success(request, self.success_message)
            return render(request, 'source_list.html')

    def get(self, request):
        return render(self.request, 'source_form.html')
