# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.core import mail

from accounts.models import User


class TestSignup(TestCase):

    def test_form_fields(self):
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

        self.assertContains(response, 'accept_terms_of_service')

    def test_bootstrap_form_control_class(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, 'form-control')

    def post_signup(self, **kwargs):
        minimal_valid_data = {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
            'accept_terms_of_service': 'on',
        }
        data = dict(minimal_valid_data)
        data.update(kwargs)
        self.client.post('/accounts/signup/', data)

    def test_successful_signup(self):
        self.post_signup(organization_url='http://example.com/foo/bar',
                         organization_town=u"Paris")
        user = User.objects.get(username='bob')
        self.assertEqual(user.organization_town, 'Paris')
        self.assertEqual(user.organization_url, 'http://example.com/foo/bar')

    def test_accepting_terms_of_service_required(self):
        self.client.post('/accounts/signup/', {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
        })
        self.assertFalse(
            User.objects.filter(username='bob').exists(),
            "We shouldn't be able to sign up without acceptiong "
            "terms of service")

    def test_email_required(self):
        self.client.post('/accounts/signup/', {
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
            'accept_terms_of_service': 'on',
        })
        self.assertFalse(
            User.objects.filter(username='bob').exists(),
            "We shouldn't be able to sign up without an email address")

    def test_send_confirmation_email(self):
        self.post_signup()
        self.assertEqual(len(mail.outbox), 1,
                         "Signup should send confirmation email")
        user = User.objects.get(username='bob')
        email_body = mail.outbox[0].body
        self.assertEqual(len(user.confirmation_code), 40)
        self.assertIn(user.confirmation_code, email_body)

    def test_user_is_not_active_without_confirmation(self):
        self.post_signup()
        user = User.objects.get(username='bob')
        self.assertFalse(user.is_active,
                         "User shouldn't be active without email confirmation")

    def test_email_confirmation_success(self):
        User.objects.create(username='bob', confirmation_code='s3cr3t')

        response = self.client.get('/accounts/confirm_email/s3cr3t/')

        self.assertContains(response, 'succès')
        user = User.objects.get(username='bob')
        self.assertTrue(user.is_active)  # Sanity check

    def test_email_confirmation_error(self):
        User.objects.create(username='bob', confirmation_code='s3cr3t')

        response = self.client.get('/accounts/confirm_email/wrong-code/')

        self.assertContains(response, 'invalide')
        user = User.objects.get(username='bob')
        self.assertFalse(user.is_active)  # Sanity check
