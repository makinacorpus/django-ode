from accounts.models import User


class LoginTestMixin(object):

    def login(self, username='bob', password='foobar'):
        self.user = User.objects.create_user(username, password=password)
        login_result = self.client.login(username=username, password=password)
        self.assertTrue(login_result)
