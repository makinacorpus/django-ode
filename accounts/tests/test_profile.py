# -*- encoding: utf-8 -*-
from django.test import TestCase

from accounts.tests.base import LoginTestMixin
from accounts.models import User


class TestProfile(LoginTestMixin, TestCase):

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
        self.client.post('/accounts/profile/', {
            'password1': 'barfoo',
            'password2': 'barfoo',
        })
        user = User.objects.get(username='bob')
        self.assertNotEqual(user.password, old_password,
                            "New password should be different")

    def test_change_password_min_length(self):
        self.login(username='bob', password='foobar')
        old_password = self.user.password
        response = self.client.post('/accounts/profile/', {
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
        response = self.client.post('/accounts/profile/', {
            'password1': 'barfoo',
            'password2': 'quuxbar',
        })
        user = User.objects.get(username='bob')
        self.assertEqual(user.password, old_password,
                         "Password should remain unchanged")
        self.assertContains(response, 'correspondent pas')

    def set_organization_attributes(self, **kwargs):
        for attrname, value in kwargs.items():
            setattr(self.user.organization, attrname, value)
        self.user.organization.save()

    def test_edit_price_information(self):
        self.login(username='bob')
        self.set_organization_attributes(price_information=u"1,50 €")

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, u"1,50 €")

    def test_update_price_information(self):
        self.login(username='bob')
        old_password = self.user.password
        response = self.client.post('/accounts/profile/', {
            'organization_price_information': u'1,25 €',
        }, follow=True)
        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.price_information, u'1,25 €')
        self.assertEqual(user.password, old_password,
                         "Password should remain unchanged")
        self.assertContains(response, u'avec succès')

    def test_edit_audience(self):
        self.login()
        self.set_organization_attributes(audience=u"Children")

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, u"Children")

    def test_update_audience(self):
        self.login(username='bob')
        response = self.client.post('/accounts/profile/',
                                    {'organization_audience': u'Children'},
                                    follow=True)
        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.audience, u'Children')
        self.assertContains(response, u'avec succès')

    def test_edit_capacity(self):
        self.login()
        self.set_organization_attributes(capacity=u"42")

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, u"42")

    def test_update_capacity(self):
        self.login(username='bob')

        self.client.post('/accounts/profile/',
                         {'organization_capacity': u'42'},
                         follow=True)

        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.capacity, u'42')

    def test_edit_activity_field(self):
        self.login()
        self.set_organization_attributes(activity_field=u"Théatre")

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, u"Théatre")

    def test_update_activity_field(self):
        self.login(username='bob')

        self.client.post('/accounts/profile/',
                         {'organization_activity_field': u'Théatre'},
                         follow=True)

        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.activity_field, u'Théatre')

    def test_update_media_url(self):
        self.login(username='bob')

        self.client.post('/accounts/profile/',
                         {'organization_media_url': u'http://example.com/'},
                         follow=True)

        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.media_url, u'http://example.com/')

    def test_update_website_url(self):
        self.login(username='bob')

        self.client.post('/accounts/profile/',
                         {'organization_website_url': u'http://example.com/'},
                         follow=True)

        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.website_url, u'http://example.com/')

    def test_update_mobile_app_name(self):
        self.login(username='bob')

        self.client.post('/accounts/profile/',
                         {'organization_mobile_app_name': u'Zoo App'},
                         follow=True)

        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.mobile_app_name, u'Zoo App')

    def test_update_other_details(self):
        self.login(username='bob')

        self.client.post('/accounts/profile/',
                         {'organization_other_details': u'foo'},
                         follow=True)

        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.other_details, u'foo')

    def verify_boolean_field(self, model_field):
        self.login(username='bob')

        self.client.post('/accounts/profile/',
                         {'organization_' + model_field: u'on'},
                         follow=True)

        user = User.objects.get(username='bob')
        self.assertTrue(getattr(user.organization, model_field))

    def test_update_is_provider(self):
        self.verify_boolean_field('is_provider')

    def test_update_is_consumer(self):
        self.verify_boolean_field('is_consumer')

    def test_update_is_host(self):
        self.verify_boolean_field('is_host')

    def test_update_is_performer(self):
        self.verify_boolean_field('is_performer')

    def test_update_is_media(self):
        self.verify_boolean_field('is_media')

    def test_update_is_creator(self):
        self.verify_boolean_field('is_creator')

    def test_update_is_website(self):
        self.verify_boolean_field('is_website')

    def test_update_is_mobile_app(self):
        self.verify_boolean_field('is_mobile_app')

    def test_update_is_other(self):
        self.verify_boolean_field('is_other')
