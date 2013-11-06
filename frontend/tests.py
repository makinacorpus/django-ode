"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, '<!doctype html>')
        self.assertContains(response, 'homepage')


class TestSources(TestCase):

    def test_source_form(self):
        response = self.client.get('/sources/new')
        self.assertContains(response, '<form action="/sources/new"')
