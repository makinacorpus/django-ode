# -*- encoding: utf-8 -*-

from django.test import TestCase

from accounts.tests.base import LoginTestMixin


class TestHeaderMenu(LoginTestMixin, TestCase):

    def test_provider_header_menu(self):

        self.login_as_provider()

        response = self.client.get('/')
        self.assertContains(response, 'Événements')
        self.assertContains(response, 'Créer')
        self.assertContains(response, 'Importer')
        self.assertContains(response, 'Exporter')
        self.assertContains(response, 'Réutilisateurs')

        self.client.logout()

    def test_consumer_header_menu(self):

        self.login_as_consumer()

        response = self.client.get('/')
        self.assertContains(response, 'Événements')
        self.assertContains(response, 'Fournisseurs')
        self.assertContains(response, 'Webservices')
        self.assertContains(response, 'Télécharger')
