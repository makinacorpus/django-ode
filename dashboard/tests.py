from django.test import TestCase

from accounts.models import User


class TestDashboard(TestCase):

    def login_as_admin(self):
        self.user = User.objects.create_superuser('admin', password='admin',
                                                  email='admin@example.com')
        return self.client.login(username='admin', password='admin')

    def test_anonymous_access(self):
        response = self.client.get('/dashboard', follow=True)
        self.assertContains(response, 'password')

    def test_login_as_superuser(self):
        self.login_as_admin()
        response = self.client.get('/dashboard', follow=True)
        self.assertContains(response, 'Structures')
