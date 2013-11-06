import requests
import json

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def create(request):
    if request.method == 'POST':
        source_data = request.POST.dict()
        source_data.pop('csrfmiddlewaretoken', None)
        post_data = {
            'sources': [source_data]
        }
        requests.post(
            settings.SOURCES_ENDPOINT,
            data=json.dumps(post_data),
            headers={
                'X-ODE-Producer-Id': request.user.id,
                'Content-Type': 'application/json',
            })
    return render(request, 'source_form.html')
