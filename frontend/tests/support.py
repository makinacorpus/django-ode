from mock import patch

from django.contrib.auth.models import User


class PatchMixin(object):
    """
    Testing utility mixin that provides methods to patch objects so that they
    will get unpatched automatically.
    """

    def patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_object(self, *args, **kwargs):
        patcher = patch.object(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_dict(self, *args, **kwargs):
        patcher = patch.dict(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def login(self):
        username, password = 'bob', 'foobar'
        self.user = User.objects.create_user(username, password=password)
        login_result = self.client.login(username=username, password=password)
        self.assertTrue(login_result)
