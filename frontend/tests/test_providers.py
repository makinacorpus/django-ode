# -*- encoding: utf-8 -*-

import json

from django.test import TestCase

from accounts.models import User, Organization
from accounts.tests.base import LoginTestMixin


class TestProviders(LoginTestMixin, TestCase):

    def setUp(self):
        self.login_as_consumer()

    def test_has_provider_listing(self):

        response = self.client.get('/provider_list/')
        self.assertContains(response, "Liste des fournisseurs")
        self.assertContains(response, "datatable-listing")

    def test_datatable_has_provider(self):

        user = User.objects.create(
            username='bob2', confirmation_code='s3cr3t', email="bob2@mc.com",
            organization=Organization.objects.create(is_provider=True))
        user.is_active = True
        user.save()

        response = self.client.get('/provider_json_list/')

        response_json = json.loads(str(response.content, encoding='UTF-8'))

        # aaData is Datatable mandatory key for displayed data
        self.assertIn('aaData', response_json.keys())
        datas = response_json['aaData']

        self.assertEqual(len(datas), 1)
