# -*- encoding: utf-8 -*-
import json

from django.conf import settings
from django.test import TestCase
from django.utils.encoding import force_text

from .support import PatchMixin
from accounts.tests.base import LoginTestMixin


class TestSources(LoginTestMixin, PatchMixin, TestCase):

    resource_name_plural = 'sources'
    end_point = settings.SOURCES_ENDPOINT

    def setUp(self):
        self.login_as_provider()
        self.requests_mock = self.patch('frontend.api_client.requests')

    def test_source_form(self):
        response = self.client.get('/imports/')
        self.assertContains(response, '<form action="/imports/"')
        self.assertNotContains(response, 'error')

    def test_create_valid_source(self):
        sample_data = {
            'url': 'http://example.com/foo',
        }

        response = self.client.post('/imports/', sample_data,
                                    follow=True)

        self.assert_post_to_api(sample_data)
        self.assertContains(response, 'alert-success')

    def test_create_invalid_source(self):
        sample_data = {
            'url': '*** invalid url ***',
        }
        response_mock = self.requests_mock.post.return_value
        response_mock.json.return_value = {
            "status": "error",
            "errors": [{
                "location": "body",
                "name": "collection.items.0.data.url",
                "description": "field error message"
            }]
        }

        response = self.client.post('/imports/', sample_data,
                                    follow=True)

        self.assert_post_to_api(sample_data)
        self.assertContains(response, 'alert-danger')
        self.assertContains(response, u'field error message')
        self.assertContains(
            response, u'value="*** invalid url ***"',
            msg_prefix="input should be pre-filled with previous input")

    def test_source_list(self):
        response_mock = self.requests_mock.get.return_value
        response_mock.json.return_value = {
            "sources": [
                {"id": 1,
                 "url": "http://example.com/source1", },
                {"id": 2,
                 "url": "http://example.com/source2", },
            ]
        }

        response = self.client.get('/sources/')

        self.requests_mock.get.assert_called_with(
            settings.SOURCES_ENDPOINT,
            headers={'X-ODE-Provider-Id': self.user.pk,
                     'Accept': 'application/json'})
        self.assertContains(response, "http://example.com/source1")
        self.assertContains(response, "http://example.com/source2")
        self.assertNotContains(
            response, "success",
            msg_prefix="not a redirect from an edition form")

    def test_datatable_source_list(self):
        response_mock = self.requests_mock.get.return_value
        response_mock.json.return_value = {
            "collection": {
                "items": [
                    {
                        "data":
                        {
                            "id": {"value": 1},
                            "url": {"value": "http://example.com/source1"}
                        }
                    },
                    {
                        "data":
                        {
                            "id": {"value": 2},
                            "url": {"value": "http://example.com/source2"}
                        }
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
