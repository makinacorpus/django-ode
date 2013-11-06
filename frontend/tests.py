from mock import patch
import json

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User


class PatchMixin(object):
    """
    Testing utility mixin that provides methods to patch objects so that they
    will get unpatched automatically.
    """

    def patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_object(self, *args, **kwargs):
        patcher = patch.object(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_dict(self, *args, **kwargs):
        patcher = patch.dict(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()


class SimpleTest(TestCase):

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, '<!doctype html>')
        self.assertContains(response, 'homepage')


class TestSources(PatchMixin, TestCase):
    sample_data = {
        'url': 'http://example.com/foo',
    }

    def login(self):
        username, password = 'bob', 'foobar'
        self.user = User.objects.create_user(username, password=password)
        login_result = self.client.login(username=username, password=password)
        self.assertTrue(login_result)

    def test_source_form(self):
        self.login()
        response = self.client.get('/sources/create')
        self.assertContains(response, '<form action="/sources/create"')

    def test_create_source(self):
        self.login()
        requests_mock = self.patch('frontend.views.sources.requests')

        self.client.post('/sources/create', self.sample_data)

        requests_mock.post.assert_called_with(
            settings.SOURCES_ENDPOINT,
            data=json.dumps({'sources': [self.sample_data]}),
            headers={'X-ODE-Producer-Id': self.user.pk,
                     'Content-Type': 'application/json'},
        )
