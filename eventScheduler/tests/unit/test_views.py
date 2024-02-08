from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from ...models import *
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
        self.client = APIClient()
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
    
class EventViewTest(BaseViewTest):
    def setUp(self):
        self.client = APIClient()
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