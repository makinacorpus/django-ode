# -*- encoding: utf-8 -*-
from django.test import TestCase

from rest_framework.authtoken.models import Token

from accounts.tests.test_factory import UserFactory


class TestApiProxy(TestCase):

    def test_anonymous_access(self):
        response = self.client.get('/api/v1/events')
        self.assertEqual(response.status_code, 401)

    def test_authenticated_access(self):
        user = UserFactory.create(is_active=True)
        token = Token.objects.create(user=user)
        response = self.client.get(
            '/api/v1/events',
            HTTP_AUTHORIZATION='Token %s' % token.key
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'v1/events')
