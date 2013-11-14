import json
from mock import patch


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

    def assert_post_to_api(self, data):
        args, kwargs = self.requests_mock.post.call_args
        self.assertEqual(args[0], self.end_point)
        self.assertEqual(json.loads(kwargs['data']),
                         {self.resource_name_plural: [data]})
        self.assertEqual(kwargs['headers'],
                         {'X-ODE-Producer-Id': self.user.pk,
                          'Content-Type': 'application/json'})
