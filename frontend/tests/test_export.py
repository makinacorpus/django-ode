# -*- encoding: utf-8 -*-
from mock import call

from django.conf import settings
from django.test import TestCase

from accounts.tests.base import LoginTestMixin
from accounts.tests.test_factory import (
    ConsumerUserFactory,
    OrganizationFactory
    )
from .support import PatchMixin


class TestExport(LoginTestMixin, PatchMixin, TestCase):

    def setUp(self):
        self.requests_mock = self.patch('frontend.api_client.requests')

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

    def test_export_json(self):
        self.login_as_consumer()
        response = self.client.post('/export/', {
            'format': 'json',
            'start_time': '',
            'end_time': ''
            })
        self.assertEqual(response.status_code, 200)
        request_args = self.requests_mock.get.call_args
        self.assertEqual(request_args, call(
            settings.EVENTS_ENDPOINT,
            headers={'X-ODE-Provider-Id': 1,
                     'Accept': 'application/vnd.collection+json'},
            params={'start_time': u'', 'end_time': u'', 'format': u'json'},
            ))

    def test_export_csv(self):
        self.login_as_consumer()
        response = self.client.post('/export/', {
            'format': 'csv',
            'start_time': '',
            'end_time': ''
            })
        self.assertEqual(response.status_code, 200)
        request_args = self.requests_mock.get.call_args
        self.assertEqual(request_args, call(
            settings.EVENTS_ENDPOINT,
            headers={'X-ODE-Provider-Id': 1,
                     'Accept': 'text/csv'},
            params={'start_time': u'', 'end_time': u'', 'format': u'csv'},
            ))

    def test_export_ics(self):
        self.login_as_consumer()
        response = self.client.post('/export/', {
            'format': 'ical',
            'start_time': '',
            'end_time': ''
            })
        self.assertEqual(response.status_code, 200)
        request_args = self.requests_mock.get.call_args
        self.assertEqual(request_args, call(
            settings.EVENTS_ENDPOINT,
            headers={'X-ODE-Provider-Id': 1,
                     'Accept': 'text/calendar'},
            params={'start_time': u'', 'end_time': u'', 'format': u'ical'},
            ))

    def test_export_with_data(self):
        self.login_as_consumer()
        response = self.client.post('/export/', {
            'format': 'json',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00'
            })
        self.assertEqual(response.status_code, 200)
        request_args = self.requests_mock.get.call_args
        self.assertEqual(request_args, call(
            settings.EVENTS_ENDPOINT,
            headers={'X-ODE-Provider-Id': 1,
                     'Accept': 'application/vnd.collection+json'},
            params={'start_time': u'2012-01-01T09:00',
                    'end_time': u'2012-01-02T18:00',
                    'format': u'json'},
            ))

    def test_export_consumers(self):
        result = (u'name,activity_field,type,address,post_code,town,url,is_med'
                  u'ia,media_url,is_website,website_url,is_mobile_app,mobile_a'
                  u'pp_name,is_other,other_details\r\nbob orga,activity,indepe'
                  u'ndant,18 rue de la rue,44000,Nantes,http://chez.bob2.com/,'
                  u'False,,True,http://media.bob2.com/,False,,False,\r\n')

        organization = OrganizationFactory(
            is_consumer=True, address='18 rue de la rue', post_code='44000',
            url='http://chez.bob2.com/', is_website=True, town='Nantes',
            website_url='http://media.bob2.com/', name='bob orga',
            activity_field='activity', type='independant', other_details='',
            mobile_app_name='', is_host=True
            )
        organization.save()
        user = ConsumerUserFactory.create(
            username='bob2', confirmation_code='s3cr3t', email="bob2@mc.com",
            organization=organization
            )
        user.is_active = True
        user.save()

        self.login_as_provider()
        response = self.client.get('/consumer_export/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/csv')
        self.assertEqual(response.content, result)

    def test_export_providers(self):
        result = (
            u'name,activity_field,type,address,post_code,town,url,is_host,is_c'
            u'reator,is_performer\r\nbob orga,activity,independant,18 rue de l'
            u'a rue,44000,Nantes,http://chez.bob2.com/,False,False,False\r\n,,'
            u',,,,,False,False,False\r\n'
            )

        organization = OrganizationFactory(
            is_provider=True, address='18 rue de la rue', post_code='44000',
            url='http://chez.bob2.com/', is_website=True, town='Nantes',
            name='bob orga', activity_field='activity', type='independant',
            )
        organization.save()
        user = ConsumerUserFactory.create(
            username='bob2', confirmation_code='s3cr3t', email="bob2@mc.com",
            organization=organization
            )
        user.is_active = True
        user.save()

        self.login_as_provider()
        response = self.client.get('/provider_export/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/csv')
        self.assertEqual(response.content, result)
