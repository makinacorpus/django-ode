from django.core.management import call_command
from django.test import TestCase
from rest_framework.authtoken.models import Token

from accounts.models import User


class TestCommands(TestCase):

    def test_create_admin(self):
        self.assertEqual(User.objects.count(), 0)

        call_command('create_admin', username='boss',
                     email='boss@example.com', password='s3cr3t',
                     organization='Acme')

        user = User.objects.get()
        self.assertTrue(user.is_superuser)
        self.assertIsNotNone(Token.objects.filter(user=user).get())
        self.assertIsNotNone(user.organization)
        self.assertEqual(user.username, 'boss')
        self.assertEqual(user.organization.name, 'Acme')
