# -*- encoding: utf-8 -*-

from django.test import TestCase

from accounts.tests.base import LoginTestMixin
from .support import PatchMixin


class TestExport(LoginTestMixin, PatchMixin, TestCase):

    def setUp(self):
        self.requests_mock = self.patch('frontend.api_client.requests')

    def _set_api_events(self):
        get_response_mock = self.requests_mock.get.return_value
        get_response_mock.json.return_value = {
            "collection": {
                "items": [{
                    "data": [
                        {'name': "id", 'value': 1},
                        {'name': "title", 'value': u"Un événement"},
                        {'name': "description", 'value': u"Description 1"},
                        {'name': "start_time", 'value': '2012-01-01T09:00'},
                        {'name': "end_time", 'value': '2012-01-02T18:00'},
                    ],
                }],
            },
        }

    def _test_export_page(self):

        response = self.client.get('/export/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Export de données')
        self.assertContains(response, 'name="start_time"')
        self.assertContains(response, 'name="format"')

    def test_provider_can_access_import(self):

        self.login_as_provider()
        self._test_export_page()
        self.client.logout()

    def test_consumer_can_access_import(self):

        self.login_as_consumer()
        self._test_export_page()
        self.client.logout()

    def test_export_json(self):
        self.login_as_consumer()
        response = self.client.post('/export/', {
            'format': 'json',
            'start_time': '',
            'end_time': ''
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(False, 'TODO')

    def test_export_csv(self):
        self.assertTrue(False, 'TODO')

    def test_export_ics(self):
        self.assertTrue(False, 'TODO')

    def test_export_with_data(self):
        self.assertTrue(False, 'TODO')
