# -*- encoding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.core import mail

from accounts.models import User
from accounts.tests.test_factory import UserFactory, ProviderUserFactory


class TestEmailConfirmation(TestCase):

    def test_consumer_only_email_confirmation_success(self):

        UserFactory.create(username='bob', confirmation_code='s3cr3t')

        response = self.client.get('/accounts/confirm_email/s3cr3t/')

        self.assertContains(response, 'succès')
        self.assertNotContains(response, 'validation')

        user = User.objects.get(username='bob')
        self.assertTrue(user.is_active,
                        "User should now be activated")

    def test_provider_email_confirmation_success(self):

        ProviderUserFactory.create(username='bob', confirmation_code='s3cr3t')

        response = self.client.get('/accounts/confirm_email/s3cr3t/')

        self.assertContains(response, 'succès')
        self.assertContains(response, 'validation')

        user = User.objects.get(username='bob')
        self.assertFalse(user.is_active,
                         "Providers shouldn't get activated automatically.")
        self.assertEqual(len(mail.outbox), 1,
                         "Email should get sent to moderator")
        email = mail.outbox[0]
        self.assertEqual(email.recipients(),
                         settings.ACCOUNTS_MODERATOR_EMAILS)
        self.assertIn(
            'http://testserver/dashboard/accounts/user/%s/' % user.pk,
            email.body)

    def test_send_provider_account_validation_email(self):
        user = ProviderUserFactory.create(username='bob',
                                          email="bob@mc.com",
                                          confirmation_code='s3cr3t')

        response = self.client.get('/accounts/confirm_email/s3cr3t/')
        self.assertContains(response, 'succès')

        # There are 2 mails in outbox

        # First one to tell admin to validate newly provider created account
        self.assertEqual(
            len(mail.outbox), 1,
            "Email should get sent to moderator")

        user.is_active = True
        user.save()

        # Second one sent when activating user via django admin
        self.assertEqual(
            len(mail.outbox), 2,
            "User must be notified that its provider account is validated.")

        email = mail.outbox[1]
        self.assertEqual(email.recipients(),
                         [user.email])
        self.assertIn(u'Votre compte fournisseur a été validé', email.body)

    def test_email_confirmation_error(self):
        UserFactory.create(username='bob', confirmation_code='s3cr3t')

        response = self.client.get('/accounts/confirm_email/wrong-code/')

        self.assertContains(response, 'invalide')
        user = User.objects.get(username='bob')
        self.assertFalse(user.is_active)
