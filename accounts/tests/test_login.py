from django.test import TestCase

from accounts.models import User


class TestLogin(TestCase):

    def test_login_form(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        User.objects.create_user(username='bob', password='foobar')
        response = self.client.post('/accounts/login/', {
            'username': 'bob',
            'password': 'foobar',
        })
        self.assertEqual(response['location'],
                         'http://testserver/accounts/profile/')

    def test_login_error(self):
        User.objects.create_user(username='bob', password='foobar')
        response = self.client.post('/accounts/login/', {
            'username': 'bob',
            'password': 'wrong-password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mot de passe')

    def test_inactive_user_cannot_login(self):
        user = User.objects.create_user(username='bob', password='foobar')
        user.is_active = False
        user.save()
        response = self.client.post('/accounts/login/', {
            'username': 'bob',
            'password': 'foobar',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'inactif')
