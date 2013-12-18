from accounts.models import User
from accounts.models import Organization


class LoginTestMixin(object):

    def logout(self):
        self.client.logout()

    def login(self, username='bob', password='foobar'):

        return self.login_as_consumer(username, password)

    def login_as_provider(self, username='bob', password='foobar'):
        organization = Organization.objects.create(is_provider=True,
                                                   is_consumer=False)
        # Adding is_active to value "True", provider accounts are not
        # activated on creation
        self.user = User.objects.create_user(username, password=password,
                                             organization=organization)
        self.user.is_active = True
        self.user.save()
        login_result = self.client.login(username=username, password=password)
        self.assertTrue(login_result)
        return self.user

    def login_as_consumer(self, username='bob', password='foobar'):
        organization = Organization.objects.create(is_provider=False,
                                                   is_consumer=True)
        self.user = User.objects.create_user(username, password=password,
                                             organization=organization)
        login_result = self.client.login(username=username, password=password)
        self.assertTrue(login_result)
        return self.user
