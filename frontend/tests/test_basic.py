# -*- encoding: utf-8 -*-
from django.test import TestCase

from accounts.tests.base import LoginTestMixin


class SimpleTest(LoginTestMixin, TestCase):

    def test_home_anonymous(self):
        response = self.client.get('/')
        self.assertContains(response, '<!DOCTYPE html>')
        self.assertContains(response, 'Connexion')
        self.assertContains(response, '/accounts/login/')
        self.assertContains(response, 'Inscription')
        self.assertContains(response, '/accounts/signup/')

    def test_home_authenticated(self):
        self.login()
        response = self.client.get('/')
        self.assertContains(response, 'Déconnexion')
        self.assertContains(response, '/accounts/logout/')
        self.assertContains(response, 'Profil')
        self.assertContains(response, '/accounts/profile/')
