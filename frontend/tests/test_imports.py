# -*- encoding: utf-8 -*-

from django.conf import settings
from django.test import TestCase

from accounts.tests.base import LoginTestMixin
from accounts.models import User
from .support import PatchMixin

events_json_data_sent = (
    '{"template": {"data": [{"name": "id", "value": "4c81f072630e11e3953c5c260'
    'a0e691e@example.com"}, {"name": "description", "value": "Description"}, {'
    '"name": "performers", "value": "artiste1, artiste2, artiste3"}, {"name": '
    '"press_url", "value": "http://presse"}, {"name": "price_information", "va'
    'lue": "tarif"}, {"name": "target", "value": "public"}, {"name": "title", '
    '"value": "Test medias"}, {"name": "start_time", "value": "2013-12-12T00:0'
    '0:00"}, {"name": "end_time", "value": "2013-12-28T00:00:00"}, {"name": "p'
    'ublication_start", "value": "2013-12-12T00:00:00"}, {"name": "publication'
    '_end", "value": "2013-12-28T00:00:00"}, {"name": "press_contact_email", "'
    'value": "aaa@aaa.aa"}, {"name": "press_contact_name", "value": "nom press'
    'e"}, {"name": "press_contact_phone_number", "value": "telephone presse"},'
    ' {"name": "ticket_contact_email", "value": "aaa@aaa.aa"}, {"name": "ticke'
    't_contact_name", "value": "nom billetterie"}, {"name": "ticket_contact_ph'
    'one_number", "value": "telephone billetterie"}, {"name": "location_name",'
    ' "value": "Nom du lieu"}, {"name": "location_address", "value": "Adresse '
    'du lieu"}, {"name": "location_post_code", "value": "Code postal"}, {"name'
    '": "location_capacity", "value": "capacite"}, {"name": "location_town", "'
    'value": "Ville"}, {"name": "location_country", "value": "Pays"}, {"name":'
    ' "tags", "value": ["tag1", "tag2", "tag3"]}, {"name": "categories", "valu'
    'e": ["category1", "category2"]}, {"name": "images", "value": [{"url": "ht'
    'tp://photo", "license": "CC BY"}, {"url": "http://photo2", "license": "CC'
    ' BY"}]}, {"name": "videos", "value": [{"url": "http://video", "license": '
    '"CC BY"}]}, {"name": "sounds", "value": [{"url": "http://audio", "license'
    '": "CC BY"}]}]}}')


class TestImports(LoginTestMixin, PatchMixin, TestCase):

    def setUp(self):
        self.requests_mock = self.patch('frontend.api_client.requests')

    def test_provider_can_access_import(self):

        self.login_as_provider()
        response = self.client.get('/imports/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Import de données')
        # Input field used to import events from a file
        self.assertContains(response, 'name="events_file"')
        # Input field used to add an event source
        self.assertContains(response, 'name="url"')
        self.assertContains(response, 'datatable-listing')
        self.client.logout()

    def test_consumer_cannot_access_import(self):

        self.login_as_consumer()
        response = self.client.get('/imports/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_superuser_can_always_access_import(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')

        response = self.client.get('/imports/')
        self.assertEqual(response.status_code, 200)

    def test_import_file_json(self):
        self.login_as_provider()
        with open('frontend/tests/resources/events.json') as fp:
            self.client.post('/imports/file/', {'events_file': fp})
            self.requests_mock.request.assert_called_with(
                "POST",
                settings.EVENTS_ENDPOINT,
                data=events_json_data_sent,
                headers={'X-ODE-Provider-Id': self.user.pk,
                         'Content-Type': 'application/vnd.collection+json',
                         'Accept-Language': 'fr'}
                )

    def test_import_file_csv(self):
        self.login_as_provider()
        with open('frontend/tests/resources/events.csv') as fp:
            self.client.post('/imports/file/', {'events_file': fp})
            fp.seek(0)
            self.requests_mock.request.assert_called_with(
                "POST",
                settings.EVENTS_ENDPOINT,
                data=fp.read(),
                headers={'X-ODE-Provider-Id': self.user.pk,
                         'Content-Type': 'application/vnd.collection+json',
                         'Accept-Language': 'fr'}
                )

    def test_import_file_ics(self):
        self.login_as_provider()
        with open('frontend/tests/resources/events.ics') as fp:
            self.client.post('/imports/file/', {'events_file': fp})
            fp.seek(0)
            self.requests_mock.request.assert_called_with(
                "POST",
                settings.EVENTS_ENDPOINT,
                data=fp.read(),
                headers={'X-ODE-Provider-Id': self.user.pk,
                         'Content-Type': 'application/vnd.collection+json',
                         'Accept-Language': 'fr'}
                )
