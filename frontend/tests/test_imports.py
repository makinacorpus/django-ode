# -*- encoding: utf-8 -*-

from django.test import TestCase

from accounts.tests.base import LoginTestMixin


class TestImports(LoginTestMixin, TestCase):

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
