import requests
import json
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class APIClient(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def get(self, ode_provider_id, mimetype="application/vnd.collection+json",
            json=True, object_id=None, *args, **kwargs):

        getkwargs = dict(
            headers={
                'X-ODE-Provider-Id': ode_provider_id,
                'Accept': mimetype,
            })

        # requests lib needs 'params' keyword for get call
        if kwargs:
            getkwargs['params'] = kwargs

        url = self.endpoint
        if object_id is not None:
            url += '/{}'.format(object_id)

        response = requests.get(url, *args, **getkwargs)

        if json:
            return response.json()
        return response.text

    def delete(self, id_to_delete, producer_id, *args, **kwargs):

        delete_url = self.endpoint + "/" + str(id_to_delete)
        response = requests.delete(
            delete_url,
            headers={
                'X-ODE-Provider-Id': producer_id,
                'Content-Type': 'application/vnd.collection+json',
                'Accept-Language': settings.LANGUAGE_CODE,
            })

        return response

    def post(self, data, provider_id,
             mimetype='application/vnd.collection+json'):
        return self.unsafe_request('POST', self.endpoint, data, provider_id,
                                   mimetype)

    def put(self, resource_id, data, provider_id,
            mimetype='application/vnd.collection+json'):
        url = "{}/{}".format(self.endpoint, resource_id)
        return self.unsafe_request('PUT', url, data, provider_id, mimetype)

    def unsafe_request(self, method, url, data, provider_id, mimetype):
        if isinstance(data, dict):
            data = json.dumps(data)
        response = requests.request(
            method,
            url,
            data=data,
            headers={
                'X-ODE-Provider-Id': provider_id,
                'Content-Type': mimetype,
                'Accept-Language': settings.LANGUAGE_CODE,
            })
        if response.status_code == 403:
            return {
                'status': 'error',
                'errors': [
                    {'name': 'events_file',
                     'description': _(u'You do not have permission to edit '
                                      u'these events.')}
                    ]
                }
        return response.json()
