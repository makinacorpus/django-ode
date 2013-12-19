# -*- encoding: utf-8 -*-
import json
from mock import call

from django.conf import settings
from django.test import TestCase
from django.utils.encoding import force_text

from .support import PatchMixin
from accounts.tests.base import LoginTestMixin


class TestEvents(LoginTestMixin, PatchMixin, TestCase):

    end_point = settings.EVENTS_ENDPOINT

    def setUp(self):
        self.login_as_provider()
        self.requests_mock = self.patch('frontend.api_client.requests')

    def test_anonymous_cannot_access_creation_form(self):
        self.logout()
        response = self.client.get('/events/create/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response['location'])

    def test_event_form(self):
        response = self.client.get('/events/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"')

    def test_create_valid_event(self):
        user_data = {
            'title': u'Un événement',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00',
        }

        response = self.client.post('/events/create/', user_data, follow=True)

        self.assert_post_to_api(user_data)
        self.assertContains(response, 'alert-success')

    def test_create_invalid_event(self):
        invalid_data = {
            'title': u'Événement',
            'start_time': '*** invalid datetime ***',
            'end_time': '2012-01-02T18:00',
        }
        response_mock = self.requests_mock.request.return_value
        response_mock.json.return_value = {
            "status": "error",
            "errors": [
                {
                    "location": "body",
                    "name": "items.0.data.start_time",
                    "description": "datetime is invalid"
                },
            ]
        }

        response = self.client.post('/events/create/', invalid_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

        self.assert_post_to_api(invalid_data)
        self.assertContains(response, 'alert-danger')
        self.assertContains(response, u'datetime is invalid', count=1)
        self.assertContains(
            response, u'value="Événement"',
            msg_prefix="input should be pre-filled with previous input")
        self.assertContains(
            response, u'value="*** invalid datetime ***"',
            msg_prefix="input should be pre-filled with previous input")

    def test_get_edit_form_not_found(self):
        get_response_mock = self.requests_mock.get.return_value
        get_response_mock.json.return_value = {
            'errors': [{'description': 'Not found'}], 'status': 404
        }
        response = self.client.get('/events/edit/BOGUS', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get_edit_form(self):
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
        response = self.client.get('/events/edit/1', follow=True)
        self.assertContains(response, u"Un événement")
        self.assertContains(response, u'action="/events/edit/1"')

    def test_post_edit_form_success(self):
        user_data = {
            'title': u'Un événement',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00',
        }

        response = self.client.post('/events/edit/1', user_data, follow=True)

        self.assert_put_to_api(resource_id='1', input_data=user_data)
        self.assertContains(response, 'alert-success')
        self.assertContains(response, u'action="/events/edit/1"')

    def test_post_edit_form_error(self):
        response_mock = self.requests_mock.request.return_value
        response_mock.json.return_value = {
            "status": "error",
            "errors": [
                {
                    "location": "body",
                    "name": "items.0.data.start_time",
                    "description": "datetime is invalid"
                },
            ]
        }
        user_data = {
            'title': u'Un événement',
            'start_time': 'BOGUS',
            'end_time': 'BOGUS',
        }

        response = self.client.post('/events/edit/1', user_data, follow=True)
        self.assert_put_to_api(resource_id='1', input_data=user_data)
        self.assertContains(response, 'alert-danger')
        self.assertContains(response, u'datetime is invalid', count=1)
        self.assertContains(response, u'action="/events/edit/1"')

    def test_event_list(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Liste des événements')
        self.assertContains(response, 'datatable-listing')

        self.client.logout()

    def test_datatable_event_list(self):
        response_mock = self.requests_mock.get.return_value
        start_t = "2013-02-02T09:00"
        start_t2 = "2013-01-02T09:00"
        end_t = "2013-02-04T19:00"
        end_t2 = "2013-01-04T19:00"
        response_mock.json.return_value = {
            "collection": {
                "items": [{
                    "data": [
                        {'name': "id", 'value': 1},
                        {'name': "title", 'value': u"Un événement"},
                        {'name': "description", 'value': u"Description 1"},
                        {'name': "start_time", 'value': start_t},
                        {'name': "end_time", 'value': end_t},
                    ],
                }, {
                    "data": [
                        {"name": "id", 'value': 2},
                        {"name": "title", 'value': u"イベント"},
                        {"name": "description", 'value': u"Description 2"},
                        {'name': "start_time", 'value': start_t2},
                        {'name': "end_time", 'value': end_t2},
                    ],
                }],
                "total_count": 2,
                "current_count": 2
            }
        }

        response = self.client.get('/events/json/')

        response_json = json.loads(force_text(response.content))
        self.requests_mock.get.assert_called_with(
            settings.EVENTS_ENDPOINT,
            headers={'X-ODE-Provider-Id': self.user.pk,
                     'Accept': 'application/vnd.collection+json'},
            params={'sort_direction': 'desc', 'offset': 0, 'limit': 10,
                    'sort_by': 'title'})

        # aaData is Datatable mandatory key for displayed data
        self.assertIn('aaData', response_json.keys())
        datas = response_json['aaData']

        self.assertEqual(len(datas), 2)

    def test_delete_invalid_event(self):
        response_mock = self.requests_mock.delete.return_value
        response_mock.status_code = 404

        sample_data = {'id_to_delete': ['123']}
        response = self.client.post('/events/delete_rows/', sample_data,
                                    follow=True)
        headers = {
            'X-ODE-Provider-Id': self.user.pk,
            'Content-Type': 'application/vnd.collection+json',
            'Accept-Language': settings.LANGUAGE_CODE,
            }
        expected = [call(settings.EVENTS_ENDPOINT + '/123', headers=headers)]
        self.assertEqual(self.requests_mock.delete.call_args_list, expected)
        self.assertEqual(response.status_code, 500)

    def test_delete_valid_event(self):
        user_data = {
            'id': '1',
            'title': u'Un événement',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00',
        }

        response = self.client.post('/events/create/', user_data, follow=True)

        self.assert_post_to_api(user_data)
        self.assertContains(response, 'alert-success')

        response_mock = self.requests_mock.delete.return_value
        response_mock.status_code = 204

        sample_data = {'id_to_delete': ['1']}
        response = self.client.post('/events/delete_rows/', sample_data,
                                    follow=True)
        headers = {
            'X-ODE-Provider-Id': self.user.pk,
            'Content-Type': 'application/vnd.collection+json',
            'Accept-Language': settings.LANGUAGE_CODE,
            }
        expected = [call(settings.EVENTS_ENDPOINT + '/1', headers=headers)]
        self.assertEqual(self.requests_mock.delete.call_args_list, expected)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Done')
