# -*- encoding: utf-8 -*-
import json
from django.test import TestCase
from django.conf import settings
from django.utils.encoding import smart_bytes

from rest_framework.authtoken.models import Token

from frontend.tests.support import PatchMixin
from accounts.tests.test_factory import UserFactory, USER_PASSWORD
from accounts.tests.test_factory import ProviderUserFactory


class TestApiProxy(PatchMixin, TestCase):

    target_url = '/'.join([settings.EVENT_API_BASE_URL, 'v1/events'])

    def setUp(self):
        self.requests_mock = self.patch('frontend.views.api_proxy.requests')
        response_mock = self.requests_mock.request.return_value
        response_mock.status_code = 200

    def make_user_with_token(self, factory):
        user = factory.create(is_active=True)
        token = Token.objects.create(user=user)
        return user, token

    def make_authenticated_request(self, method, token, url='/api/v1/events',
                                   data={}, **kwargs):
        client_method = getattr(self.client, method)
        return client_method(url, data,
                             HTTP_AUTHORIZATION='Token %s' % token.key,
                             **kwargs)

    def test_anonymous_access(self):
        response = self.client.get('/api/v1/events')
        self.assertContains(response,
                            u'Authentication credentials were not provided.',
                            status_code=401)

    def test_session_authentication(self):
        user = UserFactory.create(is_active=True)
        response = self.client.login(username=user.username,
                                     password=USER_PASSWORD)
        response = self.client.get('/api/v1/events')
        self.assertEqual(response.status_code, 200)

    def test_token_authentication(self):
        user, token = self.make_user_with_token(UserFactory)
        response = self.make_authenticated_request('get', token)
        self.assertEqual(response.status_code, 200)

    def test_get_query_string_parameters(self):
        user, token = self.make_user_with_token(UserFactory)
        data = {u'foo': u'bar'}
        self.make_authenticated_request('get', token, data=data)
        self.requests_mock.request.assert_called_with(
            'GET', self.target_url, params=data,
            headers={
                'X-ODE-API-Mount-Point': 'http://testserver/api',
            }
        )

    def test_auth_header_is_present_for_provider(self):
        user, token = self.make_user_with_token(ProviderUserFactory)
        self.make_authenticated_request('get', token)
        self.requests_mock.request.assert_called_with(
            'GET', self.target_url, headers={
                'X-ODE-Provider-Id': user.pk,
                'X-ODE-API-Mount-Point': 'http://testserver/api',
            }
        )

    def test_auth_header_is_absent_for_non_provider(self):
        user, token = self.make_user_with_token(UserFactory)
        self.make_authenticated_request('get', token)
        self.requests_mock.request.assert_called_with(
            'GET',
            self.target_url,
            headers={
                'X-ODE-API-Mount-Point': 'http://testserver/api',
            })

    def test_provider_can_make_unsafe_operation(self):
        user, token = self.make_user_with_token(ProviderUserFactory)
        data = json.dumps({'name': 'Ève'})
        for method in ('post', 'put', 'delete'):
            self.make_authenticated_request(method, token, data=data,
                                            content_type='application/json')
            self.requests_mock.request.assert_called_with(
                method.upper(), self.target_url,
                data=smart_bytes(data, 'utf-8'),
                headers={
                    'X-ODE-Provider-Id': user.pk,
                    'X-ODE-API-Mount-Point': 'http://testserver/api',
                    'CONTENT-TYPE': 'application/json',
                })

    def test_non_provider_cannot_make_unsafe_operation(self):
        user, token = self.make_user_with_token(UserFactory)
        data = json.dumps({'name': 'Ève'})
        for method in ('post', 'put', 'delete'):
            response = self.make_authenticated_request(
                'post', token, data=data, content_type='application/json')
            self.assertContains(
                response,
                u"You do not have permission to perform this action.",
                status_code=403)

    def _test_accept_header(self, accept_header):
        user, token = self.make_user_with_token(ProviderUserFactory)
        response = self.make_authenticated_request('get',
                                                   token,
                                                   HTTP_ACCEPT='text/csv')
        self.assertEqual(response.status_code, 200)
        self.requests_mock.request.assert_called_with(
            'GET', self.target_url, headers={
                'X-ODE-Provider-Id': user.pk,
                'X-ODE-API-Mount-Point': 'http://testserver/api',
                'ACCEPT': 'text/csv',
            }
        )

    def test_csv(self):
        self._test_accept_header('text/csv')

    def test_calendar(self):
        self._test_accept_header('text/calendar')

    def test_collection_json(self):
        self._test_accept_header('application/vnd.collection+json')
