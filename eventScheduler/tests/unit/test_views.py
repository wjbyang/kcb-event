from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from ...views import *
from ..test_data_generators.views_generator import *

class BaseViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def assert_post_status(self, post_url, mock_serializer, request_data, expected_status_code, expected_response_data):
        response = self.client.post(post_url, request_data, format='json')
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.data, expected_response_data)
        mock_serializer.assert_called_once_with(data=request_data)
        mock_serializer.return_value.is_valid.assert_called_once()

class UserViewTest(BaseViewTest):
    def setUp(self):
        self.post_url = '/eventScheduler/v1/user/'

    @patch('eventScheduler.views.UserSerializer', **{ 
        'return_value.is_valid.return_value': True,
        'return_value.save.return_value': None
    })
    def test_post_user_success(self, mock_serializer):
        expected_response_data = UserData().server_response_format()
        expected_status_code = status.HTTP_201_CREATED
        mock_serializer.return_value.validated_data = expected_response_data
        request_data = UserData().request_format()
        self.assert_post_status(self.post_url, mock_serializer, request_data, expected_status_code, expected_response_data)

    @patch('eventScheduler.views.UserSerializer', **{ 
        'return_value.is_valid.return_value': False,
        'return_value.errors': {
            'first_name': ['This field is required'], 
            'email': ['This field is required.'],
            'organization_id': ['This field is required.'],
        }
    })
    def test_post_user_fail(self, mock_serializer):
        expected_response_data = {
            'first_name': ['This field is required'], 
            'email': ['This field is required.'],
            'organization_id': ['This field is required.'],
        }
        expected_status_code = status.HTTP_400_BAD_REQUEST
        request_data = UserData().missing('first_name','email','organization_id')
        self.assert_post_status(self.post_url, mock_serializer, request_data, expected_status_code, expected_response_data)

class ViewUserTest(BaseViewTest):
    @patch('eventScheduler.views.UserSerializer')
    @patch('eventScheduler.views.User.objects')
    def test_get_user_success(self, mock_User, mock_serializer):
        mock_User.get.return_value = 'some-non-json-object'
        expected_response_data = UserData().server_response_format()
        mock_serializer.return_value.data = expected_response_data
        user_id = expected_response_data['guid']
        get_url = f"/eventScheduler/v1/user/{user_id}/"
        response = self.client.get(get_url, format='json')
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_User.get.assert_called_once_with(guid=user_id)
        mock_serializer.assert_called_once_with(mock_User.get.return_value)

class ViewUsersTest(BaseViewTest):
    @patch('eventScheduler.views.UserSerializer')
    @patch('eventScheduler.views.User.objects')
    def test_get_users_success(self, mock_User, mock_serializer):
        mock_User.all.return_value = 'some-queryset-object'
        user1 = UserData().server_response_format()
        user2 = UserData().server_response_format()
        user2['email'] = 'different-email@something.com'
        expected_response_data = [user1, user2]
        mock_serializer.return_value.data = expected_response_data
        get_url = f"/eventScheduler/v1/users/"
        response = self.client.get(get_url, format='json')
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_User.all.assert_called_once()
        mock_serializer.assert_called_once_with(mock_User.all.return_value, many=True)

class UpdateUserTest(BaseViewTest):
    

class EventViewTest(BaseViewTest):
    def setUp(self):
        self.post_url = '/eventScheduler/v1/event/'

    @patch('eventScheduler.views.EventSerializer', **{ 
        'return_value.is_valid.return_value': True,
        'return_value.save.return_value': None
    })
    def test_post_event_success(self, mock_serializer):
        expected_response_data = EventData().server_response_format()
        expected_status_code = status.HTTP_201_CREATED
        mock_serializer.return_value.validated_data = expected_response_data
        request_data = EventData().request_format()
        self.assert_post_status(self.post_url, mock_serializer, request_data, expected_status_code, expected_response_data)

    @patch('eventScheduler.views.EventSerializer', **{ 
        'return_value.is_valid.return_value': False,
        'return_value.errors': {
            'name': ['This field is required'], 
            'location': ['This field is required.'],
            'description': ['This field is required.'],
            'start_time': ['This field is required.'],
        }
    })
    def test_post_event_fail(self, mock_serializer):
        expected_response_data = {
            'name': ['This field is required'], 
            'location': ['This field is required.'],
            'description': ['This field is required.'],
            'start_time': ['This field is required.'],
        }
        request_data = EventData().missing('name', 'location', 'description', 'start_time')
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assert_post_status(self.post_url, mock_serializer, request_data, expected_status_code, expected_response_data)

class ViewEventTest(BaseViewTest):
    @patch('eventScheduler.views.EventSerializer')
    @patch('eventScheduler.views.Event.objects')
    def test_get_event_success(self, mock_Event, mock_serializer):
        mock_Event.get.return_value = 'some-non-json-object'
        expected_response_data = EventData().server_response_format()
        mock_serializer.return_value.data = expected_response_data
        event_id = expected_response_data['guid']
        get_url = f"/eventScheduler/v1/event/{event_id}/"
        response = self.client.get(get_url, format='json')
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_Event.get.assert_called_once_with(guid=event_id)
        mock_serializer.assert_called_once_with(mock_Event.get.return_value)

class ViewEventsTest(BaseViewTest):
    @patch('eventScheduler.views.EventSerializer')
    @patch('eventScheduler.views.Event.objects')
    def test_get_events_success(self, mock_Event, mock_serializer):
        mock_Event.all.return_value = 'some-queryset-object'
        event1 = UserData().server_response_format()
        event2 = UserData().server_response_format()
        expected_response_data = [event1, event2]
        mock_serializer.return_value.data = expected_response_data
        get_url = f"/eventScheduler/v1/events/"
        response = self.client.get(get_url, format='json')
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_Event.all.assert_called_once()
        mock_serializer.assert_called_once_with(mock_Event.all.return_value, many=True)