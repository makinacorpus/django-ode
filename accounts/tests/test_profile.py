# -*- encoding: utf-8 -*-
from django.test import TestCase

from accounts.tests.base import LoginTestMixin
from accounts.models import User


class TestProfile(LoginTestMixin, TestCase):

    def test_login_required(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'],
            'http://testserver/accounts/login/?next=/accounts/profile/')

    def test_get_form(self):
        self.login()
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, '<legend>Connexion</legend>')
        self.assertContains(response, 'password1')

    def test_change_password_success(self):
        self.login(username='bob', password='foobar')
        old_password = self.user.password
        self.client.post('/accounts/profile/', {
            'password1': 'barfoo',
            'password2': 'barfoo',
        })
        user = User.objects.get(username='bob')
        self.assertNotEqual(user.password, old_password,
                            "New password should be different")

    def test_change_password_error(self):
        self.login(username='bob', password='foobar')
        old_password = self.user.password
        response = self.client.post('/accounts/profile/', {
            'password1': 'barfoo',
            'password2': 'quux',
        })
        user = User.objects.get(username='bob')
        self.assertEqual(user.password, old_password,
                         "Password should remain unchanged")
        self.assertContains(response, 'correspondent pas')

    def test_edit_price_information(self):
        self.login(username='bob')
        self.user.organization.price_information = u"1,50 €"
        self.user.organization.save()

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, u"1,50 €")

    def test_update_price_information(self):
        self.login(username='bob')
        old_password = self.user.password
        response = self.client.post('/accounts/profile/', {
            'price_information': u'1,25 €',
        }, follow=True)
        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.price_information, u'1,25 €')
        self.assertEqual(user.password, old_password,
                         "Password should remain unchanged")
        self.assertContains(response, u'avec succès')
