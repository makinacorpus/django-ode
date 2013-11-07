from django.test import TestCase

from .support import PatchMixin


class TestEvents(PatchMixin, TestCase):

    def test_anonymous_cannot_access_creation_form(self):
        response = self.client.get('/events/create')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response['location'])

    def test_event_form(self):
        self.login()
        response = self.client.get('/events/create')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"')
