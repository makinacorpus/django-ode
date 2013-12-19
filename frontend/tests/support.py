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

    def assert_post_to_api(self, input_data):
        args, kwargs = self.requests_mock.post.call_args
        self.assertEqual(args[0], self.end_point)
        posted_json = json.loads(kwargs['data'])
        posted_data_as_dict = {
            field['name']: field['value']
            for field in posted_json['template']['data']
        }
        for key, value in input_data.items():
            self.assertIn(key, posted_data_as_dict.keys())
            if isinstance(value, dict):
                self.assertDictEqual(value, posted_data_as_dict[key])
            else:
                self.assertEqual(value, posted_data_as_dict[key])
        self.assertEqual(kwargs['headers'], {
            'X-ODE-Provider-Id': self.user.pk,
            'Content-Type': 'application/vnd.collection+json',
            'Accept-Language': 'fr',
        })
