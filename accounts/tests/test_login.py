from django.test import TestCase

from accounts.tests.test_factory import UserFactory


class TestLogin(TestCase):

    def test_login_form(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        user = UserFactory.create(username='bob', password='foobar')
        user.is_active = True
        user.save()

        response = self.client.post('/accounts/login/', {
            'username': 'bob',
            'password': 'foobar',
        })

        self.assertEqual(response['location'],
                         'http://testserver/accounts/profile/')

    def test_login_error(self):
        UserFactory.create(username='bob', password='foobar')
        response = self.client.post('/accounts/login/', {
            'username': 'bob',
            'password': 'wrong-password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mot de passe')

    def test_inactive_user_cannot_login(self):
        UserFactory.create(username='bob',
                           password='foobar',
                           is_active=False)

        response = self.client.post('/accounts/login/', {
            'username': 'bob',
            'password': 'foobar',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'inactif')
