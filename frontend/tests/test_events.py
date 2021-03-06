# -*- encoding: utf-8 -*-
import json
from mock import call

from django.conf import settings
from django.test import TestCase
from django.utils.encoding import force_text

from .support import PatchMixin
from frontend.views.base import data_list_to_dict
from accounts.tests.base import LoginTestMixin
from accounts.tests.test_factory import (
    ProviderUserFactory,
    ProviderOrganizationFactory
    )


class TestEvents(LoginTestMixin, PatchMixin, TestCase):

    end_point = settings.EVENTS_ENDPOINT

    def setUp(self):
        self.login_as_provider()
        self.requests_mock = self.patch('frontend.api_client.requests')


class TestEvent(TestEvents):

    def setup_response(self):
        response_mock = self.requests_mock.get.return_value
        start_t = "2013-02-02T09:00"
        end_t = "2013-02-04T19:00"
        response_mock.json.return_value = {
            "collection": {
                "items": [{
                    "data": [
                        {'name': "id", 'value': 1},
                        {'name': "title", 'value': u"Un événement"},
                        {'name': "description", 'value': u"Description 1"},
                        {'name': "start_time", 'value': start_t},
                        {'name': "end_time", 'value': end_t},
                    ],
                }],
                "total_count": 1,
                "current_count": 1
            }
        }

    def test_view_valid_event(self):
        self.setup_response()
        response = self.client.get('/events/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"Description 1")
        self.assertContains(response, u"Le 02/02/2013 à 09h00")
        self.assertContains(response, u"Le 04/02/2013 à 19h00")
        self.assertNotContains(response, u"Médias")
        self.assertNotContains(response, u"Billeterie")
        self.assertNotContains(response, u"Lieu")
        self.assertNotContains(response, u"Tags")
        self.assertNotContains(response, u"Catégories")

    def test_view_invalid_event(self):
        response_mock = self.requests_mock.get.return_value
        response_mock.json.return_value = {
            "errors": [{u'description': u'Not found'}],
            u'status': 404
        }
        response = self.client.get('/events/123456/')
        self.assertContains(response,
                            u"L'événement correspondant n'a pas été trouvé.")


class TestCreate(TestEvents):

    def test_anonymous_cannot_access_creation_form(self):
        self.logout()
        response = self.client.get('/events/create/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response['location'])

    def test_event_form(self):
        response = self.client.get('/events/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"')

    def test_create_valid_event(self):
        self.logout()
        self.login_as_provider(username="provider", first_name='john',
                               last_name="doe", email="john.doe@example.com",
                               phone_number="0123456789")
        user_data = {
            'title': u'Un événement',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00',
            'tags': '',
            'categories': ', foo, bar\n,\r',
        }

        response = self.client.post('/events/create/', user_data, follow=True)

        api_data = {
            'firstname': 'john',
            'lastname': 'doe',
            'email': 'john.doe@example.com',
            'telephone': '0123456789',
            'language': 'fr',
            }
        api_data.update(user_data)
        api_data['tags'] = []
        api_data['categories'] = ['foo', 'bar']

        self.assert_post_to_api(api_data)
        self.assertContains(response, 'alert-success')

    def test_create_event_with_media(self):
        user_data = {
            'title': u'Un événement',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00',
            'media_photo': 'http://photo',
            'media_photo_license': 'CC BY',
            'media_photo2': 'http://photo2',
            'media_photo_license2': 'CC BY',
            'media_video': 'http://video',
            'media_video_license': 'unknown',
            'media_audio': 'http://audio',
            'media_audio_license': 'CC BY',
        }

        response = self.client.post('/events/create/', user_data, follow=True)

        api_data = {
            'title': u'Un événement',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00',
            'images': [
                {'url': 'http://photo', 'license': 'CC BY'},
                {'url': 'http://photo2', 'license': 'CC BY'},
                ],
            'videos': [{'url': 'http://video', 'license': 'unknown'}],
            'sounds': [{'url': 'http://audio', 'license': 'CC BY'}]
            }

        self.assert_post_to_api(api_data)
        self.assertContains(response, 'alert-success')

    def test_create_invalid_event(self):
        invalid_data = {
            'title': u'Événement',
            'start_time': '*** invalid datetime ***',
            'end_time': '2012-01-02T18:00',
        }
        response_mock = self.requests_mock.request.return_value
        response_mock.json.return_value = {
            "status": "error",
            "errors": [
                {
                    "location": "body",
                    "name": "items.0.data.start_time",
                    "description": "datetime is invalid"
                },
            ]
        }

        response = self.client.post('/events/create/', invalid_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

        self.assert_post_to_api(invalid_data)
        self.assertContains(response, 'alert-danger')
        self.assertContains(response, u'datetime is invalid', count=1)
        self.assertContains(
            response, u'value="Événement"',
            msg_prefix="input should be pre-filled with previous input")
        self.assertContains(
            response, u'value="*** invalid datetime ***"',
            msg_prefix="input should be pre-filled with previous input")


class TestEdit(TestEvents):

    def test_get_edit_form_not_found(self):
        get_response_mock = self.requests_mock.get.return_value
        get_response_mock.json.return_value = {
            'errors': [{'description': 'Not found'}], 'status': 404
        }
        response = self.client.get('/events/edit/BOGUS', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get_edit_form(self):
        get_response_mock = self.requests_mock.get.return_value
        get_response_mock.json.return_value = {
            "collection": {
                "items": [{
                    "data": [
                        {'name': "id", 'value': 1},
                        {'name': "title", 'value': u"Un événement"},
                        {'name': "description", 'value': u"Description 1"},
                        {'name': "start_time", 'value': '2012-01-01T09:00'},
                        {'name': "end_time", 'value': '2012-01-04T18:00'},
                        {'name': "tags", 'value': ['tag1', 'tag2']},
                        {'name': "categories",
                         'value': ['category1', 'category2']},
                    ],
                }],
            },
        }
        response = self.client.get('/events/edit/1', follow=True)
        self.assertContains(response, u"Un événement")
        self.assertContains(response, u'action="/events/edit/1/"')
        self.assertContains(response, u'tag1, tag2')
        self.assertContains(response, u'category1, category2')
        self.assertContains(response, u'01/01/2012 09:00 - 04/01/2012 18:00')

    def test_get_edit_form_for_event_without_tags(self):
        get_response_mock = self.requests_mock.get.return_value
        get_response_mock.json.return_value = {
            "collection": {
                "items": [{
                    "data": [
                        {'name': "id", 'value': 1},
                        {'name': "title", 'value': u"Un événement"},
                        {'name': "description", 'value': u"Description 1"},
                        {'name': "start_time", 'value': '2012-01-01T09:00'},
                        {'name': "end_time", 'value': '2012-01-04T18:00'},
                        {'name': "categories",
                         'value': ['category1', 'category2']},
                    ],
                }],
            },
        }
        response = self.client.get('/events/edit/1', follow=True)
        self.assertContains(response, u"Un événement")

    def test_post_edit_form_success(self):
        user_data = {
            'title': u'Un événement',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00',
        }

        response = self.client.post('/events/edit/1/', user_data, follow=True)

        self.assert_put_to_api(resource_id='1', input_data=user_data)
        self.assertContains(response, 'alert-success')
        self.assertContains(response, u'Liste des événements')

    def test_post_edit_form_error(self):
        response_mock = self.requests_mock.request.return_value
        response_mock.json.return_value = {
            "status": "error",
            "errors": [
                {
                    "location": "body",
                    "name": "items.0.data.start_time",
                    "description": "datetime is invalid"
                },
            ]
        }
        user_data = {
            'title': u'Un événement',
            'start_time': 'BOGUS',
            'end_time': 'BOGUS',
        }

        response = self.client.post('/events/edit/1/', user_data)
        self.assert_put_to_api(resource_id='1', input_data=user_data)
        self.assertContains(response, 'alert-danger')
        self.assertContains(response, u'datetime is invalid', count=1)
        self.assertContains(response, u'action="/events/edit/1/"')


class TestDelete(TestEvents):

    def test_delete_invalid_event(self):
        response_mock = self.requests_mock.delete.return_value
        response_mock.status_code = 404

        sample_data = {'ids': ['123']}
        response = self.client.post('/events/delete_rows/', sample_data,
                                    follow=True)
        headers = {
            'X-ODE-Provider-Id': self.user.pk,
            'Content-Type': 'application/vnd.collection+json',
            'Accept-Language': settings.LANGUAGE_CODE,
            }
        expected = [call(settings.EVENTS_ENDPOINT + '/123', headers=headers)]
        self.assertEqual(self.requests_mock.delete.call_args_list, expected)
        self.assertEqual(response.status_code, 500)

    def test_delete_valid_event(self):
        user_data = {
            'id': '1',
            'title': u'Un événement',
            'start_time': '2012-01-01T09:00',
            'end_time': '2012-01-02T18:00',
        }

        response = self.client.post('/events/create/', user_data, follow=True)

        self.assert_post_to_api(user_data)
        self.assertContains(response, 'alert-success')

        response_mock = self.requests_mock.delete.return_value
        response_mock.status_code = 204

        sample_data = {'ids': ['1']}
        response = self.client.post('/events/delete_rows/', sample_data,
                                    follow=True)
        headers = {
            'X-ODE-Provider-Id': self.user.pk,
            'Content-Type': 'application/vnd.collection+json',
            'Accept-Language': settings.LANGUAGE_CODE,
            }
        expected = [call(settings.EVENTS_ENDPOINT + '/1', headers=headers)]
        self.assertEqual(self.requests_mock.delete.call_args_list, expected)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Done')


class TestDuplicate(TestEvents):
    event_data = [
        {'name': "title", 'value': u"Un événement"},
        {'name': "description", 'value': u"Description 1"},
        {'name': "start_time", 'value': "2013-02-02T09:00"},
        {'name': "end_time", 'value': "2013-02-04T19:00"},
    ]

    def setup_get_response(self, event_ids):
        response_mock = self.requests_mock.get.return_value
        response_mock.json.side_effect = [
            {
                "collection": {
                    "items": [{
                        "data": [
                            {'name': "id",
                             'value': event_id}
                        ] + self.event_data,
                    }],
                    "total_count": 1,
                    "current_count": 1
                }
            }
            for event_id in event_ids
        ]

    def assert_get_from_api(self, event_id):
        event_url = u"{}/{}".format(self.end_point, event_id)
        self.requests_mock.get.assert_any_call(
            event_url,
            headers={
                'X-ODE-Provider-Id': self.user.id,
                'Accept': 'application/vnd.collection+json',
            })

    def test_duplicate_valid_event(self):
        event_ids = [1, 2]
        self.setup_get_response(event_ids)

        response = self.client.post('/events/duplicate_rows/',
                                    {'ids': event_ids},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assert_get_from_api(event_id=1)
        self.assert_get_from_api(event_id=2)
        self.assert_post_to_api(data_list_to_dict(self.event_data))
        self.assert_post_to_api(data_list_to_dict(self.event_data))


class TestList(TestEvents):

    def setup_response_with_two_events(self):
        response_mock = self.requests_mock.get.return_value
        start_t = "2013-02-02T09:00"
        start_t2 = "2013-01-02T09:00"
        end_t = "2013-02-04T19:00"
        end_t2 = "2013-01-04T19:00"
        response_mock.json.return_value = {
            "collection": {
                "items": [{
                    "data": [
                        {'name': "id", 'value': 1},
                        {'name': "title", 'value': u"Un événement"},
                        {'name': "description", 'value': u"Description 1"},
                        {'name': "start_time", 'value': start_t},
                        {'name': "end_time", 'value': end_t},
                    ],
                }, {
                    "data": [
                        {"name": "id", 'value': 2},
                        {"name": "title", 'value': u"イベント"},
                        {"name": "description", 'value': u"Description 2"},
                        {'name': "start_time", 'value': start_t2},
                        {'name': "end_time", 'value': end_t2},
                    ],
                }],
                "total_count": 2,
                "current_count": 2
            }
        }

    def assertGetRequestWithParams(self, params):
        self.requests_mock.get.assert_called_with(
            settings.EVENTS_ENDPOINT,
            headers={'X-ODE-Provider-Id': self.user.pk,
                     'Accept': 'application/vnd.collection+json'},
            params=params)

    def extract_aaData(self, response):
        response_json = json.loads(force_text(response.content))
        # aaData is Datatable mandatory key for displayed data
        self.assertIn('aaData', response_json.keys())
        return response_json['aaData']

    def assertFirstCellEqual(self, items, expected):
        self.assertCellEqual(items, 0, expected)

    def assertCellEqual(self, items, index, expected):
        last_cell = items[0][index]
        self.assertEqual(last_cell, expected)

    def test_event_list(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Liste des événements')
        self.assertContains(response, 'datatable-listing')
        self.assertContains(response, 'event-list-subnav nav nav-tabs')

    def test_user_event_list(self):
        response = self.client.get('/events/user/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Liste des événements')
        self.assertContains(response, 'datatable-listing')
        self.assertContains(response, 'event-list-subnav nav nav-tabs')

    def test_event_list_as_consumer(self):
        self.logout()
        self.login_as_consumer('bob2')
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Liste des événements')
        self.assertContains(response, 'datatable-listing')
        self.assertNotContains(response, 'event-list-subnav nav nav-tabs')
        self.assertNotContains(response, u'datatable-delete-rows')

    def test_user_event_list_as_consumer(self):
        self.logout()
        self.login_as_consumer('bob2')
        response = self.client.get('/events/user/')
        self.assertEqual(response.status_code, 403)

    def test_datatable_all_event_list(self):
        self.setup_response_with_two_events()

        response = self.client.get('/events/json/')

        self.assertGetRequestWithParams({
            'sort_direction': 'desc',
            'offset': 0,
            'limit': 10,
            'sort_by': 'title',
        })

        aaData_items = self.extract_aaData(response)
        self.assertEqual(len(aaData_items), 2)
        self.assertFirstCellEqual(
            aaData_items,
            u'<a data-toggle="modal" data-target="#events-modal" '
            u'href="/events/1/">Un événement</a>')

    def test_datatable_user_event_list(self):
        self.setup_response_with_two_events()

        response = self.client.get('/events/user/json/')

        self.assertGetRequestWithParams({
            'sort_direction': 'desc',
            'offset': 0,
            'limit': 10,
            'sort_by': 'title',
            'provider_id': 1,
        })
        aaData_items = self.extract_aaData(response)
        self.assertEqual(len(aaData_items), 2)
        self.assertFirstCellEqual(
            aaData_items,
            u'<a href="/events/edit/1/">Un événement</a>')
        self.assertCellEqual(
            aaData_items,
            5,
            u'<input type="checkbox" class="datatable-delete"'
            u' data-id="1">')
        self.assertCellEqual(
            aaData_items,
            6,
            u'<input type="checkbox" class="datatable-duplicate"'
            u' data-id="1">')

    def test_datatable_all_event_list_with_provider(self):
        response_mock = self.requests_mock.get.return_value
        start_t = "2013-02-02T09:00"
        end_t = "2013-02-04T19:00"
        response_mock.json.return_value = {
            "collection": {
                "items": [{
                    "data": [
                        {'name': "id", 'value': 1},
                        {'name': "title", 'value': u"Un événement"},
                        {'name': "description", 'value': u"Description 1"},
                        {'name': "start_time", 'value': start_t},
                        {'name': "end_time", 'value': end_t},
                        {'name': 'provider_id', 'value': '2'}
                    ],
                }],
                "total_count": 1,
                "current_count": 1
            }
        }
        org_host = ProviderOrganizationFactory.create(
            is_host=True, town="town_host", activity_field='act1',
            name='host_organization'
            )
        user = ProviderUserFactory.create(
            username='bob2', confirmation_code='s3cr3t', email="bob2@mc.com",
            organization=org_host)
        user.is_active = True
        user.save()

        response = self.client.get('/events/json/')
        aaData_items = self.extract_aaData(response)
        self.assertEqual(len(aaData_items), 1)
        self.assertEqual(aaData_items[0][3],
                         u'<a data-toggle="modal" data-target="#events-modal" '
                         u'href="/provider/2/">host_organization</a>')


class TestUtils(TestCase):

    def test_convert_iso_to_listing_date(self):
        from frontend.views.events import convert_iso_to_listing_date
        iso_date = "2012-01-16T19:00:00"
        human_date = "Le 16/01/2012 à 19h00"
        self.assertEqual(
            convert_iso_to_listing_date(iso_date),
            human_date
        )
