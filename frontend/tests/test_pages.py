from django.test import TestCase
from rest_framework.authtoken.models import Token

from accounts.tests.test_factory import UserFactory, USER_PASSWORD


class TestPages(TestCase):

    def test_webservices(self):
        user = UserFactory.create(is_active=True)
        token = Token.objects.create(user=user)
        self.client.login(username=user.username, password=USER_PASSWORD)
        response = self.client.get('/webservices/')
        self.assertContains(response, token.key)
        self.assertContains(response, 'http://testserver/api')

    def test_404(self):
        response = self.client.get('/foo/bar/quux/')
        self.assertContains(response, 'site_logo.png', status_code=404)
