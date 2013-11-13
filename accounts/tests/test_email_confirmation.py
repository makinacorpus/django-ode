from django.conf import settings
from django.test import TestCase
from django.core import mail

from accounts.models import User


class TestEmailConfirmation(TestCase):

    def test_email_confirmation_success(self):
        User.objects.create(username='bob', confirmation_code='s3cr3t')

        response = self.client.get('/accounts/confirm_email/s3cr3t/')

        self.assertContains(response, 'succès')
        user = User.objects.get(username='bob')
        self.assertTrue(user.is_active,
                        "User should now be activated")

    def test_provider_email_confirmation_success(self):
        User.objects.create(username='bob', confirmation_code='s3cr3t',
                            is_provider=True)

        response = self.client.get('/accounts/confirm_email/s3cr3t/')

        self.assertContains(response, 'succès')
        user = User.objects.get(username='bob')
        self.assertFalse(user.is_active,
                         "Providers shouldn't get activated automatically.")
        self.assertEqual(len(mail.outbox), 1,
                         "Email should get sent to moderator")
        email = mail.outbox[0]
        self.assertEqual(email.recipients(),
                         settings.ACCOUNTS_MODERATOR_EMAILS)
        self.assertIn('http://testserver/admin/accounts/user/%s/' % user.pk,
                      email.body)

    def test_email_confirmation_error(self):
        User.objects.create(username='bob', confirmation_code='s3cr3t')

        response = self.client.get('/accounts/confirm_email/wrong-code/')

        self.assertContains(response, 'invalide')
        user = User.objects.get(username='bob')
        self.assertFalse(user.is_active)
