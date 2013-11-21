# -*- encoding: utf-8 -*-
import os

from django.test import TestCase

from accounts.tests.base import LoginTestMixin
from accounts.models import User, Contact


class TestProfile(LoginTestMixin, TestCase):

    def post_with_required_params(self, params):
        required_params = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'email': 'bob@example.com',
            'phone_number': '123456789',
        }
        required_params.update(params)
        return self.client.post('/accounts/profile/', required_params,
                                follow=True)

    def _test_update_organization_char_field(self, field_name, value,
                                             login=True):
        if login:
            self.login(username='bob')

        self.post_with_required_params({'organization_' + field_name: value})

        user = User.objects.get(username='bob')
        self.assertEqual(getattr(user.organization, field_name), value)

    def _test_update_char_field(self, field_name, value, login=True):
        if login:
            self.login(username='bob')

        self.post_with_required_params({field_name: value})

        user = User.objects.get(username='bob')
        self.assertEqual(getattr(user, field_name), value)

    def _test_update_char_field_as_consumer(self, field_name, value):
        user = self.login(username='bob')
        user.organization.is_consumer = True
        user.organization.save()
        self._test_update_organization_char_field(field_name, value,
                                                  login=False)

    def _test_update_boolean_field(self, model_field, login=True):
        if login:
            self.login(username='bob')

        self.post_with_required_params({'organization_' + model_field: u'on'})

        user = User.objects.get(username='bob')
        self.assertTrue(getattr(user.organization, model_field))

    def _test_update_boolean_field_as(self, model_field, flag):
        user = self.login(username='bob')
        setattr(user.organization, flag, True)
        user.organization.save()

        self._test_update_boolean_field(model_field, login=False)

    def _test_update_boolean_field_as_provider(self, model_field):
        self._test_update_boolean_field_as(model_field, flag='is_provider')

    def _test_update_boolean_field_as_consumer(self, model_field):
        self._test_update_boolean_field_as(model_field, flag='is_consumer')

    def _test_prefilled_organization_field(self, field_name, value):
        self.login(username='bob')
        setattr(self.user.organization, field_name, value)
        self.user.organization.save()

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, value)

    def _test_prefilled_field(self, field_name, value):
        self.login(username='bob')
        setattr(self.user, field_name, value)
        self.user.save()

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, value)

    def _test_edit_contact(self, contact_type, field, value):
        user = self.login(username='bob')
        setattr(user.organization, contact_type,
                Contact.objects.create(**{field: value}))
        user.organization.save()

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, value)

    def _test_update_contact(self, contact_type, field, value):
        self.login(username='bob')

        field_name = '{}_{}_{}'.format('organization', contact_type, field)
        self.post_with_required_params({field_name: value})

        organization = User.objects.get(username='bob').organization
        contact = getattr(organization, contact_type)
        self.assertEqual(getattr(contact, field), value)

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
        self.assertContains(response, '<legend>CONNEXION</legend>')
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
        self._test_prefilled_organization_field('price_information', u"1,50 €")

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
        self._test_prefilled_organization_field('audience', u"Children")

    def test_update_audience(self):
        self._test_update_organization_char_field('audience', u'Children')

    def test_edit_capacity(self):
        self._test_prefilled_organization_field('capacity', u"42")

    def test_update_capacity(self):
        self._test_update_organization_char_field('capacity', u'42')

    def test_edit_main_contact_last_name(self):
        self._test_prefilled_field('last_name', 'Dupont')

    def test_update_main_contact_last_name(self):
        self._test_update_char_field('last_name', 'Dupont')

    def test_edit_main_contact_first_name(self):
        self._test_prefilled_field('first_name', u'Éric')

    def test_edit_main_contact_email(self):
        self._test_prefilled_field('email', u'bob@example.com')

    def test_update_main_contact_email(self):
        self._test_update_char_field('email', u'bob@example.com')

    def test_edit_main_contact_phone_number(self):
        self._test_prefilled_field('phone_number', u'1234567890')

    def test_update_main_contact_phone_number(self):
        self._test_update_char_field('phone_number', u'1234567890')

    def test_update_main_contact_first_name(self):
        self._test_update_char_field('first_name', u'Éric')

    def test_edit_activity_field(self):
        self._test_prefilled_organization_field('activity_field', u"Théatre")

    def test_edit_ticket_contact_name(self):
        self._test_edit_contact('ticket_contact', 'name', value=u'Bob Smith')

    def test_update_ticket_contact_name(self):
        self._test_update_contact('ticket_contact', 'name', u'Alice Robert')

    def test_edit_ticket_contact_email(self):
        self._test_edit_contact('ticket_contact', 'email',
                                value=u'bob@example.com')

    def test_update_ticket_contact_email(self):
        self._test_update_contact('ticket_contact', 'email',
                                  u'bob@example.com')

    def test_edit_ticket_contact_phone_number(self):
        self._test_edit_contact('ticket_contact', 'phone_number',
                                value=u'1234556678')

    def test_update_ticket_contact_phone_number(self):
        self._test_update_contact('ticket_contact', 'phone_number',
                                  u'1234556678')

    def test_edit_press_contact_name(self):
        self._test_edit_contact('press_contact', 'name', value=u'Bob Smith')

    def test_update_press_contact_name(self):
        self._test_update_contact('press_contact', 'name', u'Alice Robert')

    def test_edit_press_contact_email(self):
        self._test_edit_contact('press_contact', 'email',
                                value=u'bob@example.com')

    def test_update_press_contact_email(self):
        self._test_update_contact('press_contact', 'email', u'bob@example.com')

    def test_edit_press_contact_phone_number(self):
        self._test_edit_contact('press_contact', 'phone_number',
                                value=u'1234556678')

    def test_update_press_contact_phone_number(self):
        self._test_update_contact('press_contact', 'phone_number',
                                  u'1234556678')

    def test_update_activity_field(self):
        self._test_update_organization_char_field('activity_field', u'Théatre')

    def test_update_media_url(self):
        self._test_update_char_field_as_consumer('media_url',
                                                 u'http://example.com/')

    def test_update_website_url(self):
        self._test_update_char_field_as_consumer('website_url',
                                                 u'http://example.com/')

    def test_update_mobile_app_name(self):
        self._test_update_char_field_as_consumer('mobile_app_name', u'Zoé App')

    def test_update_other_details(self):
        self._test_update_char_field_as_consumer('other_details', u'foo')

    def test_update_is_provider_has_no_effect(self):
        self.login(username='bob')

        self.post_with_required_params({'organization_is_provider': u'on'})

        user = User.objects.get(username='bob')
        self.assertFalse(user.organization.is_provider)

    def test_update_is_consumer_has_no_effect(self):
        self.login_as_provider(username='bob')

        self.post_with_required_params({'organization_is_consumer': u'on'})

        user = User.objects.get(username='bob')
        self.assertFalse(user.organization.is_consumer)

    def test_update_is_host(self):
        self._test_update_boolean_field_as_provider('is_host')

    def test_update_is_performer(self):
        self._test_update_boolean_field_as_provider('is_performer')

    def test_update_is_creator(self):
        self._test_update_boolean_field_as_provider('is_creator')

    def test_update_is_media(self):
        self._test_update_boolean_field_as_consumer('is_media')

    def test_update_is_website(self):
        self._test_update_boolean_field_as_consumer('is_website')

    def test_update_is_mobile_app(self):
        self._test_update_boolean_field_as_consumer('is_mobile_app')

    def test_update_is_other(self):
        self._test_update_boolean_field_as_consumer('is_other')

    def test_provider_can_see_event_creator_checkbox(self):
        user = self.login()
        user.organization.is_provider = True
        user.organization.save()

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, u"Créateur")
        self.assertContains(response, u"accueil")
        self.assertContains(response, u"artiste")

    def test_non_provider_cannot_see_event_creator_checkbox(self):
        self.login()

        response = self.client.get('/accounts/profile/')

        self.assertNotContains(response, u"Créateur")
        self.assertNotContains(response, u"accueil")
        self.assertNotContains(response, u"artiste")

    def test_consumer_can_see_event_creator_checkbox(self):
        user = self.login()
        user.organization.is_consumer = True
        user.organization.save()

        response = self.client.get('/accounts/profile/')

        self.assertContains(response, u"un media print")
        self.assertContains(response, u"Site web")
        self.assertContains(response, u"Application mobile")
        self.assertContains(response, u"Autre")

    def test_non_consumer_cannot_see_event_creator_checkbox(self):
        self.login_as_provider()

        response = self.client.get('/accounts/profile/')

        self.assertNotContains(response, u"un media print")
        self.assertNotContains(response, u"Site web")
        self.assertNotContains(response, u"Application mobile")
        self.assertNotContains(response, u"Autre")

    def test_cannot_select_provider_type_if_not_provider(self):
        self.login()

        self.post_with_required_params({
            'organization_is_host': 'on',
            'organization_is_performer': 'on',
            'organization_is_creator': 'on',
        })
        organization = User.objects.filter(username='bob').get().organization
        self.assertFalse(organization.is_provider)
        self.assertFalse(organization.is_host)
        self.assertFalse(organization.is_performer)
        self.assertFalse(organization.is_creator)

    def test_cannot_select_consumer_type_if_not_consumer(self):
        self.login_as_provider()

        self.post_with_required_params({
            'organization_is_media': 'on',
            'organization_is_website': 'on',
            'organization_is_mobile_app': 'on',
            'organization_is_other': 'on',
        })
        organization = User.objects.filter(username='bob').get().organization
        self.assertFalse(organization.is_media)
        self.assertFalse(organization.is_website)
        self.assertFalse(organization.is_mobile_app)
        self.assertFalse(organization.is_other)

    def test_ticket_contact(self):
        user = self.login()
        user.organization.ticket_contact = Contact.objects.create(name=u'Bob')
        user.organization.save()

        user = User.objects.get(username='bob')
        self.assertEqual(user.organization.ticket_contact.name, u'Bob')

    def _post_picture(self, filename='site_logo.png'):
        here = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(here, 'data', filename)
        with open(filename, 'rb') as fp:
            self.post_with_required_params({
                'organization_picture': fp,
            })

    def test_update_picture(self):
        self.login()
        self._post_picture()
        user = User.objects.get(username='bob')
        self.assertTrue(user.organization.picture.name.endswith('.png'))

    def test_edit_picture_no_profile_picutre_set(self):
        self.login()
        response = self.client.get('/accounts/profile/')
        self.assertContains(response, 'profile_picture_placeholder.png')

    def test_edit_picture_profile_picutre_set(self):
        self.login()
        self._post_picture('site_logo.png')
        response = self.client.get('/accounts/profile/')
        self.assertContains(response, 'site_logo.png')

    def test_delete_picture(self):
        self.login()
        self.post_with_required_params({
            'organization_picture-clear': 'on',
        })
        response = self.client.get('/accounts/profile/')
        self.assertContains(response, 'profile_picture_placeholder.png')
        self.assertNotContains(
            response, 'Actuellement:',
            msg_prefix="We don't want to display the existing file URL")
