#-*- coding: utf-8 -*-
import re

from django.test import TestCase
from django.core import mail

from accounts.tests.test_factory import UserFactory


class TestReset(TestCase):

    def test_reset_form(self):
        response = self.client.get('/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_reset_form_send_email(self):
        user = UserFactory.create(username='bob', password='foobar')
        user.is_active = True
        user.save()

        response = self.client.post('/accounts/password_reset/', {
            'email': 'bob@example.com'
        })

        self.assertEqual(response['location'],
                         'http://testserver/accounts/password_reset_done/')
        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body
        self.assertIn('Une demande de nouveau mot de passe', email_body)

    def test_reset_form_complete(self):
        user = UserFactory.create(username='bob', password='foobar')
        user.is_active = True
        user.save()

        response = self.client.post('/accounts/password_reset/', {
            'email': 'bob@example.com'
        })
        email_body = mail.outbox[0].body
        m = re.search('(/accounts/password_reset_confirm/[^\n]+)\n',
                      email_body)
        self.assertIsNotNone(m)
        url = m.group(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, {
            'new_password1': 'barfoo',
            'new_password2': 'barfoo'
        })
        self.assertEqual(response['location'],
                         'http://testserver/accounts/password_reset_complete/')
        response = self.client.post('/accounts/login/', {
            'username': 'bob',
            'password': 'barfoo',
        })
        self.assertEqual(response['location'],
                         'http://testserver/accounts/profile/')
