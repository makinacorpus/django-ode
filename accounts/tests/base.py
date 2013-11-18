from accounts.models import User
from accounts.models import Organization


class LoginTestMixin(object):

    def login(self, username='bob', password='foobar'):
        organization = Organization.objects.create()
        self.user = User.objects.create_user(username, password=password,
                                             organization=organization)
        login_result = self.client.login(username=username, password=password)
        self.assertTrue(login_result)
