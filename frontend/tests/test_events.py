# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.conf import settings

from .support import PatchMixin
from frontend.views.events import merge_datetime


class TestEvents(PatchMixin, TestCase):

    resource_name_plural = 'events'
    end_point = settings.EVENTS_ENDPOINT

    def setUp(self):
        self.requests_mock = self.patch('frontend.api_client.requests')

    def test_anonymous_cannot_access_creation_form(self):
        response = self.client.get('/events/create')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response['location'])

    def test_event_form(self):
        self.login()
        response = self.client.get('/events/create')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"')

    def test_create_valid_event(self):
        self.login()
        user_data = {
            'title': u'Un événement',
            'start_date': '2012-01-01',
            'start_time': '09:00',
            'end_date': '2012-01-02',
            'end_time': '18:00',
        }

        response = self.client.post('/events/create', user_data, follow=True)

        api_data = dict(user_data)
        merge_datetime(api_data)
        self.assert_post_to_api(api_data)
        self.assertContains(response, 'alert-success')

    def test_create_invalid_event(self):
        self.login()
        invalid_data = {
            'title': u'Événement',
            'start_date': '*** invalid date ***',
            'start_time': '09:00',
            'end_date': '2012-01-02',
            'end_time': '18:00',
        }
        response_mock = self.requests_mock.post.return_value
        response_mock.json.return_value = {
            "status": "error",
            "errors": [
                {
                    "location": "body",
                    "name": "events.0.start_date",
                    "description": "date is invalid"
                },
            ]
        }

        response = self.client.post('/events/create', invalid_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

        api_data = dict(invalid_data)
        merge_datetime(api_data)
        self.assert_post_to_api(api_data)
        self.assertContains(response, 'alert-error')
        self.assertContains(response, u'date is invalid', count=1)
        self.assertContains(
            response, u'value="Événement"',
            msg_prefix="input should be pre-filled with previous input")
        self.assertContains(
            response, u'value="*** invalid date ***"',
            msg_prefix="input should be pre-filled with previous input")

    def test_event_list(self):
        self.login()
        response_mock = self.requests_mock.get.return_value
        response_mock.json.return_value = {
            "events": [
                {
                    "id": 1,
                    "title": u"Un événement",
                    "start_time": "2013-02-02T09:00",
                    "end_time": "2013-02-04T19:00",
                },
                {
                    "id": 2,
                    "title": u"イベント",
                    "start_time": "2013-01-02T09:00",
                    "end_time": "2013-01-04T19:00",
                },
            ]
        }

        response = self.client.get('/events')

        self.assertEqual(response.status_code, 200)
        self.requests_mock.get.assert_called_with(
            settings.EVENTS_ENDPOINT,
            headers={'X-ODE-Producer-Id': self.user.pk,
                     'Accept': 'application/json'})
        self.assertContains(response, u"Un événement")
        self.assertContains(response, u"イベント")
        self.assertContains(response, u"2013-02-02T09:00")
        self.assertContains(response, u"2013-01-04T19:00")
        self.assertNotContains(
            response, "success",
            msg_prefix="not a redirect from an edition form")
