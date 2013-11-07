from django.test import TestCase


class SimpleTest(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, '<!DOCTYPE html>')
        self.assertContains(response, 'homepage')
