# -*- encoding: utf-8 -*-

from django.test import TestCase

from accounts.tests.base import LoginTestMixin


class TestExport(LoginTestMixin, TestCase):

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
