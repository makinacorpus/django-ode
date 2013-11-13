from django.test import TestCase

from accounts.models import User


class SimpleTest(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, '<!DOCTYPE html>')
        self.assertContains(response, 'Connexion')
        self.assertContains(response, '/accounts/login/')
        self.assertContains(response, 'Inscription')
        self.assertContains(response, '/accounts/signup/')

    def test_home_authenticated(self):
        User.objects.create_user(username='bob', password='foobar')
        self.client.login(username='bob', password='foobar')
        response = self.client.get('/')
        self.assertContains(response, 'Déconnexion')
        self.assertContains(response, '/accounts/logout/')
