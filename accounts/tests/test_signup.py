# -*- encoding: utf-8 -*-
from django.test import TestCase

from accounts.models import User


class TestSignup(TestCase):

    def test_profile_fields(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, 'is_provider')
        self.assertContains(response, 'is_host')
        self.assertContains(response, 'is_creator')
        self.assertContains(response, 'is_performer')

        self.assertContains(response, 'is_consumer')
        self.assertContains(response, 'is_media')
        self.assertContains(response, 'media_url')
        self.assertContains(response, 'is_website')
        self.assertContains(response, 'website_url')
        self.assertContains(response, 'is_mobile_app')
        self.assertContains(response, 'mobile_app_name')
        self.assertContains(response, 'is_other')
        self.assertContains(response, 'other_details')

        self.assertContains(response, 'organization_type')
        self.assertContains(response, 'organization_activity_field')
        self.assertContains(response, 'organization_name')
        self.assertContains(response, 'organization_address')
        self.assertContains(response, 'organization_post_code')
        self.assertContains(response, 'organization_town')
        self.assertContains(response, 'organization_url')

        self.assertContains(response, 'last_name')
        self.assertContains(response, 'first_name')
        self.assertContains(response, 'email')
        self.assertContains(response, 'phone_number')

        self.assertContains(response, 'username')
        self.assertContains(response, 'password')

    def test_bootstrap_form_control_class(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, 'form-control')

    def test_signup_creates_user(self):
        self.client.post('/accounts/signup/', {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
            'organization_url': 'http://example.com/foo/bar',
            'organization_town': u"Paris",
        })
        user = User.objects.filter(username='bob').get()
        self.assertEqual(user.organization_town, 'Paris')
        self.assertEqual(user.organization_url, 'http://example.com/foo/bar')
