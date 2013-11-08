# -*- encoding: utf-8 -*-
from django.test import TestCase


class TestSignup(TestCase):

    def test_profile_fields(self):
        self.skipTest('not implemented')
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, 'is_provider')
        self.assertContains(response, 'is_consumer')

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
