# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.conf import settings

from .support import PatchMixin
from frontend.views.events import merge_datetime


class TestEvents(PatchMixin, TestCase):

    resource_name_plural = 'events'
    end_point = settings.EVENTS_ENDPOINT

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
        self.requests_mock = self.patch('frontend.views.base.requests')
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
