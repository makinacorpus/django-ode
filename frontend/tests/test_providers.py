# -*- encoding: utf-8 -*-

import json

from django.utils.encoding import force_text
from django.test import TestCase

from accounts.tests.base import LoginTestMixin
from accounts.tests.test_factory import ProviderUserFactory


class TestProviders(LoginTestMixin, TestCase):

    def setUp(self):
        self.login_as_consumer()

    def test_has_provider_listing(self):

        response = self.client.get('/provider_list/')
        self.assertContains(response, "Liste des fournisseurs")
        self.assertContains(response, "datatable-listing")

    def test_datatable_has_provider(self):

        user = ProviderUserFactory.create(
            username='bob2', confirmation_code='s3cr3t', email="bob2@mc.com")
        user.is_active = True
        user.save()

        response = self.client.get('/provider_json_list/')

        response_json = json.loads(force_text(response.content))

        # aaData is Datatable mandatory key for displayed data
        self.assertIn('aaData', response_json.keys())
        datas = response_json['aaData']

        self.assertEqual(len(datas), 1)
