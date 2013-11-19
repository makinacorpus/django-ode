# -*- encoding: utf-8 -*-
from django.test import TestCase

from accounts.tests.base import LoginTestMixin
from accounts.models import User


class TestProfile(LoginTestMixin, TestCase):

    def post_with_required_params(self, params):
        required_params = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'email': 'bob@example.com',
            'phone_number': '123456789',
        }
        params.update(required_params)
        return self.client.post('/accounts/profile/', params, follow=True)

    def _test_update_char_field(self, field_name, value):
        self.login(username='bob')

        self.post_with_required_params({'organization_' + field_name: value})

        user = User.objects.get(username='bob')
        self.assertEqual(getattr(user.organization, field_name), value)

    def _test_update_boolean_field(self, model_field):
        self.login(username='bob')

        self.post_with_required_params({'organization_' + model_field: u'on'})

        user = User.objects.get(username='bob')
        self.assertTrue(getattr(user.organization, model_field))

    def _test_prefilled_field(self, field_name, value):
        self.login(username='bob')
        setattr(self.user.organization, field_name, value)
        self.user.organization.save()

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, value)

    def test_login_required(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'],
            'http://testserver/accounts/login/?next=/accounts/profile/')

    def test_get_form(self):
        self.login()
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, '<legend>Connexion</legend>')
        self.assertContains(response, 'password1')

    def test_change_password_success(self):
        self.login(username='bob', password='foobar')
        old_password = self.user.password
        self.post_with_required_params({
            'password1': 'barfoo',
            'password2': 'barfoo',
        })
        user = User.objects.get(username='bob')
        self.assertNotEqual(user.password, old_password,
                            "New password should be different")

    def test_change_password_min_length(self):
        self.login(username='bob', password='foobar')
        old_password = self.user.password
        response = self.post_with_required_params({
            'password1': 'barfo',
            'password2': 'barfo',
        })
        user = User.objects.get(username='bob')
        self.assertEqual(user.password, old_password,
                         "Password should remain unchanged")
        self.assertContains(response, 'au moins')

    def test_change_password_error(self):
        self.login(username='bob', password='foobar')
        old_password = self.user.password
        response = self.post_with_required_params({
            'password1': 'barfoo',
            'password2': 'quuxbar',
        })
        user = User.objects.get(username='bob')
        self.assertEqual(user.password, old_password,
                         "Password should remain unchanged")
        self.assertContains(response, 'correspondent pas')

    def test_edit_price_information(self):
        self._test_prefilled_field('price_information', u"1,50 €")

    def test_update_price_information(self):
        self.login(username='bob')
        old_password = self.user.password
        response = self.post_with_required_params({
            'organization_price_information': u'1,25 €',
        })
        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.price_information, u'1,25 €')
        self.assertEqual(user.password, old_password,
                         "Password should remain unchanged")
        self.assertContains(response, u'avec succès')

    def test_edit_audience(self):
        self._test_prefilled_field('audience', u"Children")

    def test_update_audience(self):
        self._test_update_char_field('audience', u'Children')

    def test_edit_capacity(self):
        self._test_prefilled_field('capacity', u"42")

    def test_update_capacity(self):
        self._test_update_char_field('capacity', u'42')

    def test_edit_activity_field(self):
        self._test_prefilled_field('activity_field', u"Théatre")

    def test_update_activity_field(self):
        self._test_update_char_field('activity_field', u'Théatre')

    def test_update_media_url(self):
        self._test_update_char_field('media_url', u'http://example.com/')

    def test_update_website_url(self):
        self._test_update_char_field('website_url', u'http://example.com/')

    def test_update_mobile_app_name(self):
        self._test_update_char_field('mobile_app_name', u'Zoé App')

    def test_update_other_details(self):
        self._test_update_char_field('other_details', u'foo')

    def test_update_is_provider_has_no_effect(self):
        self.login(username='bob')

        self.post_with_required_params({'organization_is_provider': u'on'})

        user = User.objects.get(username='bob')
        self.assertFalse(user.organization.is_provider)

    def test_update_is_consumer_has_no_effect(self):
        self.login(username='bob')

        self.post_with_required_params({'organization_is_consumer': u'on'})

        user = User.objects.get(username='bob')
        self.assertFalse(user.organization.is_consumer)

    def test_update_is_host(self):
        self._test_update_boolean_field('is_host')

    def test_update_is_performer(self):
        self._test_update_boolean_field('is_performer')

    def test_update_is_media(self):
        self._test_update_boolean_field('is_media')

    def test_update_is_creator(self):
        self._test_update_boolean_field('is_creator')

    def test_update_is_website(self):
        self._test_update_boolean_field('is_website')

    def test_update_is_mobile_app(self):
        self._test_update_boolean_field('is_mobile_app')

    def test_update_is_other(self):
        self._test_update_boolean_field('is_other')
