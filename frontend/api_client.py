import requests
import json


class APIClient(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def post(self, data, producer_id):
        response = requests.post(
            self.endpoint,
            data=json.dumps(data),
            headers={
                'X-ODE-Producer-Id': producer_id,
                'Content-Type': 'application/json',
            })
        return response.json()

    def get(self, producer_id):
        response = requests.get(
            self.endpoint,
            headers={
                'X-ODE-Producer-Id': producer_id,
                'Accept': 'application/json',
            })
        return response.json()
