# -*- encoding: utf-8 -*-
import json
from mock import call

from django.conf import settings
from django.test import TestCase
from django.utils.encoding import force_text

from .support import PatchMixin
from accounts.tests.base import LoginTestMixin


class TestSources(LoginTestMixin, PatchMixin, TestCase):

    end_point = settings.SOURCES_ENDPOINT

    def setUp(self):
        self.login_as_provider()
        self.requests_mock = self.patch('frontend.api_client.requests')

    def test_source_form(self):
        response = self.client.get('/imports/')
        self.assertContains(response, '<form action="/imports/source/"')
        self.assertNotContains(response, 'error')

    def test_create_valid_source(self):
        sample_data = {
            'url': 'http://example.com/foo',
        }

        response = self.client.post('/imports/source/', sample_data,
                                    follow=True)

        self.assert_post_to_api(sample_data)
        self.assertContains(response, 'alert-success')

    def test_create_invalid_source(self):
        sample_data = {
            'url': '*** invalid url ***',
        }
        response_mock = self.requests_mock.request.return_value
        response_mock.json.return_value = {
            "status": "error",
            "errors": [{
                "location": "body",
                "name": "items.0.data.url",
                "description": "field error message"
            }]
        }

        response = self.client.post('/imports/source/', sample_data,
                                    follow=True)

        self.assert_post_to_api(sample_data)
        self.assertContains(response, 'alert-danger')
        self.assertContains(response, u'field error message')
        self.assertContains(
            response, u'value="*** invalid url ***"',
            msg_prefix="input should be pre-filled with previous input")

    def test_datatable_source_list(self):
        response_mock = self.requests_mock.get.return_value
        response_mock.json.return_value = {
            "collection": {
                "items": [
                    {
                        "data": [
                            {"name": "id", "value": 1},
                            {"name": "url",
                             "value": "http://example.com/source1"}
                        ]
                    },
                    {
                        "data": [
                            {"name": "id", "value": 2},
                            {"name": "url",
                             "value": "http://example.com/source2"}
                        ]
                    }
                ],
                "total_count": 2,
                "current_count": 2,
            }
        }

        response = self.client.get('/sources/json/')
        response_json = json.loads(force_text(response.content))

        # aaData is Datatable mandatory key for displayed data
        self.assertIn('aaData', response_json.keys())
        datas = response_json['aaData']

        self.assertEqual(len(datas), 2)

    def test_delete_invalid_source(self):
        response_mock = self.requests_mock.delete.return_value
        response_mock.status_code = 404

        sample_data = {
            'id_to_delete': ['123456'],
        }

        response = self.client.post('/sources/delete_rows/', sample_data,
                                    follow=True)
        self.requests_mock.delete.assert_called_with(
            settings.SOURCES_ENDPOINT + '/123456',
            headers={
                'X-ODE-Provider-Id': self.user.pk,
                'Content-Type': 'application/vnd.collection+json',
                'Accept-Language': 'fr',
            })

        self.assertEqual(response.status_code, 500)

    def test_delete_valid_source(self):

        sample_data = {
            'url': 'http://example.com/foo',
        }
        response = self.client.post('/imports/source/', sample_data,
                                    follow=True)

        sample_data_2 = {
            'url': 'http://example2.com/foo',
        }
        response = self.client.post('/imports/source/', sample_data_2,
                                    follow=True)

        response_mock = self.requests_mock.delete.return_value
        response_mock.status_code = 204

        sample_data = {
            'id_to_delete': ['1', '2'],
        }

        response = self.client.post('/sources/delete_rows/', sample_data,
                                    follow=True)
        headers = {
            'X-ODE-Provider-Id': self.user.pk,
            'Content-Type': 'application/vnd.collection+json',
            'Accept-Language': settings.LANGUAGE_CODE,
        }
        expected = [
            call(settings.SOURCES_ENDPOINT + '/1', headers=headers),
            call(settings.SOURCES_ENDPOINT + '/2', headers=headers),
        ]
        self.assertEqual(self.requests_mock.delete.call_args_list, expected)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Done')
