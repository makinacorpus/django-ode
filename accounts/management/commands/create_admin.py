from optparse import make_option

from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from accounts.models import User, Organization


class Command(BaseCommand):
    help = "Create an admin account with an organization and an API token"
    option_list = BaseCommand.option_list + (
        make_option('--username',
                    action='store',
                    default='admin',
                    dest='username',
                    help='Admin user name (Default: %default)'),
        make_option('--email',
                    action='store',
                    default='admin@example.com',
                    dest='email',
                    help='Admin email address (Default: %default)'),
        make_option('--password',
                    action='store',
                    default='admin',
                    dest='password',
                    help='Admin password (Default: %default)'),
        make_option('--organization',
                    default='ODE',
                    action='store',
                    dest='organization',
                    help='Name of the admin organization (Default: %default)'),
    )

    def handle(self, *args, **options):
        organization = Organization.objects.create(
            name=options['organization'])

        user = User.objects.create_superuser(options['username'],
                                             options['email'],
                                             options['password'],
                                             organization=organization)
        Token.objects.create(user=user)
