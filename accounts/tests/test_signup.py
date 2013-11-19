# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail

from accounts.models import User


class TestSignup(TestCase):

    def post_signup(self, **kwargs):
        minimal_valid_data = {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
            'accept_terms_of_service': 'on',
            'organization_is_provider': 'on',
        }
        data = dict(minimal_valid_data)
        data.update(kwargs)
        return self.client.post('/accounts/signup/', data, follow=True)

    def test_form_fields(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, 'organization_is_provider')
        self.assertContains(response, 'organization_is_consumer')
        self.assertContains(response, 'organization_is_host')
        self.assertContains(response, 'organization_is_creator')
        self.assertContains(response, 'organization_is_performer')

        self.assertContains(response, 'organization_is_media')
        self.assertContains(response, 'media_url')
        self.assertContains(response, 'organization_is_website')
        self.assertContains(response, 'website_url')
        self.assertContains(response, 'organization_is_mobile_app')
        self.assertContains(response, 'mobile_app_name')
        self.assertContains(response, 'organization_is_other')
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

    def test_successful_signup(self):
        response = self.post_signup(
            organization_name=u'Évé',
            organization_activity_field=u'Théatre',
            organization_url='http://example.com/foo/bar',
            organization_price_information='4 €',
            organization_town=u"Paris",
            organization_type=u"individual",
            organization_address=u"65 Baker Street",
            organization_post_code=u"123 ABC",
            organization_is_provider='on',
        )

        user = User.objects.get(username='bob')

        self.assertEqual(user.organization.name, u'Évé')
        self.assertEqual(user.organization.activity_field, u'Théatre')
        self.assertEqual(user.organization.price_information, u'4 €')
        self.assertEqual(user.organization.type, u'individual')
        self.assertEqual(user.organization.address, u'65 Baker Street')
        self.assertEqual(user.organization.post_code, u'123 ABC')
        self.assertEqual(user.organization.town, 'Paris')
        self.assertEqual(user.organization.url, 'http://example.com/foo/bar')
        self.assertTrue(user.organization.is_provider)
        self.assertContains(response, 'email de confirmation')

    def test_successful_provider_signup(self):
        response = self.post_signup(organization_is_provider=True)
        user = User.objects.get(username='bob')
        self.assertTrue(user.organization.is_provider)
        self.assertContains(response, 'modérateur')

    def test_accepting_terms_of_service_required(self):
        self.client.post('/accounts/signup/', {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
            'organization_is_provider': 'on',
        })
        self.assertFalse(
            User.objects.filter(username='bob').exists(),
            "We shouldn't be able to sign up without acceptiong "
            "terms of service")

    def test_redisplay_form_keeps_consumer_selected(self):
        response = self.client.post('/accounts/signup/', {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'barfoo',
            'organization_is_consumer': 'on',
        })
        self.assertContains(
            response,
            '<div id="is-consumer-details" class="subchoices collapse in">')

    def test_redisplay_form_keeps_provider_selected(self):
        response = self.client.post('/accounts/signup/', {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'barfoo',
            'organization_is_provider': 'on',
        })
        self.assertContains(
            response,
            '<div id="is-provider-details" class="subchoices collapse in">')

    def test_email_required(self):
        self.client.post('/accounts/signup/', {
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
            'accept_terms_of_service': 'on',
            'organization_is_provider': 'on',
        })
        self.assertFalse(
            User.objects.filter(username='bob').exists(),
            "We shouldn't be able to sign up without an email address")

    def test_provider_or_consumer_required(self):
        response = self.client.post('/accounts/signup/', {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
            'accept_terms_of_service': 'on',
        })
        self.assertFalse(
            User.objects.filter(username='bob').exists(),
            "We shouldn't be able to sign up without "
            "being a provider or a consumer")
        self.assertContains(response, "fournisseur ou consommateur")

    def test_consumer_can_sign_up(self):
        self.client.post('/accounts/signup/', {
            'email': 'bob@example.com',
            'username': 'bob',
            'password1': 'foobar',
            'password2': 'foobar',
            'accept_terms_of_service': 'on',
            'organization_is_provider': 'on',
        })
        self.assertTrue(User.objects.filter(username='bob').exists())

    def test_send_confirmation_email(self):
        self.post_signup()
        self.assertEqual(len(mail.outbox), 1,
                         "Signup should send confirmation email")
        user = User.objects.get(username='bob')
        email_body = mail.outbox[0].body
        self.assertEqual(len(user.confirmation_code), 40)
        confirmation_url = 'http://testserver' + reverse(
            'accounts:confirm_email', kwargs={
                'confirmation_code': user.confirmation_code
            })
        self.assertIn(confirmation_url, email_body)

    def test_user_is_not_active_without_confirmation(self):
        self.post_signup()
        user = User.objects.get(username='bob')
        self.assertFalse(user.is_active,
                         "User shouldn't be active without email confirmation")
