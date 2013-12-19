# -*- encoding: utf-8 -*-

import json

from django.utils.encoding import force_text
from django.utils.translation import string_concat
from django.test import TestCase

from accounts.models import Organization
from accounts.tests.base import LoginTestMixin
from accounts.tests.test_factory import (
    ProviderUserFactory,
    ProviderOrganizationFactory
    )


class TestProviders(LoginTestMixin, TestCase):

    def setUp(self):
        self.login_as_consumer()

    def test_has_provider_listing(self):

        response = self.client.get('/provider_list/')
        self.assertContains(response, "Liste des fournisseurs")
        self.assertContains(response, "datatable-listing")

    def test_has_provider_view(self):

        user = ProviderUserFactory.create(
            username='bob2', confirmation_code='s3cr3t', email="bob2@mc.com")
        user.is_active = True
        user.save()

        response = self.client.get('/provider/1/')
        self.assertNotContains(response, "modal")
        self.assertContains(response, "Type de structure")

    def test_provider_ajax_view(self):

        user = ProviderUserFactory.create(
            username='bob2', confirmation_code='s3cr3t', email="bob2@mc.com")
        user.is_active = True
        user.save()

        response = self.client.get('/provider/1/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, "modal")
        self.assertContains(response, "Type de structure")

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

    def test_datatable_columns_values(self):

        org_host = ProviderOrganizationFactory.create(
            is_host=True, town="town_host", activity_field='act1',
            name='host_organization'
            )
        user = ProviderUserFactory.create(
            username='bob2', confirmation_code='s3cr3t', email="bob2@mc.com",
            organization=org_host)
        user.is_active = True
        user.save()

        org_creator_performer = ProviderOrganizationFactory.create(
            is_creator=True, is_performer=True, town="town_creator",
            activity_field='act2', name="creator_organization"
            )
        user2 = ProviderUserFactory.create(
            username='bob3', confirmation_code='s3cr3t', email="bob3@mc.com",
            organization=org_creator_performer)
        user2.is_active = True
        user2.save()

        response = self.client.get('/provider_json_list/')
        response_json = json.loads(force_text(response.content))
        # aaData is Datatable mandatory key for displayed data
        self.assertIn('aaData', response_json.keys())
        datas = response_json['aaData']
        self.assertEqual(len(datas), 2)

        # Test user
        self.assertIn('host_organization', datas[0][0])
        self.assertIn('modal', datas[0][0])
        self.assertEqual(datas[0][2], Organization.PROVIDERS_DICT['host'])
        self.assertEqual(datas[0][3], 'act1')
        self.assertEqual(datas[0][4], 'town_host')

        # Test user2
        self.assertIn('creator_organization', datas[1][0])
        self.assertIn('modal', datas[1][0])
        vocation = string_concat(Organization.PROVIDERS_DICT['creator'], ', ',
                                 Organization.PROVIDERS_DICT['performer'])
        self.assertEqual(datas[1][2], vocation)
        self.assertEqual(datas[1][3], 'act2')
        self.assertEqual(datas[1][4], 'town_creator')
