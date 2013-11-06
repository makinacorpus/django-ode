from django.test import TestCase


class SimpleTest(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, '<!doctype html>')
        self.assertContains(response, 'homepage')

