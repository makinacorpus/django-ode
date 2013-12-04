import requests
import json


class APIClient(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def post(self, data, provider_id):
        response = requests.post(
            self.endpoint,
            data=json.dumps(data),
            headers={
                'X-ODE-Provider-Id': provider_id,
                'Content-Type': 'application/json',
            })
        return response.json()

    def get(self, provider_id, *args, **kwargs):

        getkwargs = dict(
            headers={
                'X-ODE-Provider-Id': provider_id,
                'Accept': 'application/json',
            })

        # requests lib needs 'params' keyword for get call
        if kwargs:
            getkwargs['params'] = kwargs

        response = requests.get(self.endpoint, *args, **getkwargs)

        return response.json()

    def delete(self, id_to_delete, producer_id, *args, **kwargs):

        delete_url = self.endpoint + "/" + str(id_to_delete)
        response = requests.delete(
            delete_url,
            headers={
                'X-ODE-Provider-Id': producer_id,
                'Content-Type': 'application/json',
            })

        return response
