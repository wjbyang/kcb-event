from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from django.utils import timezone
from ..models.models import *
from ..views import *

class UserViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_url = '/eventScheduler/v1/user/post/'
        self.valid_data = {
            'first_name': 'random-valid-first-name',
            'last_name': 'random-valid-last-name',
            'email': 'random-valid-email',
            'organization_id': 'random-valid-organization-id'
        }

    @patch('eventScheduler.views.get_organization_data')
    @patch('eventScheduler.views.UserSerializer')
    def test_post_user_success(self, mock_serializer, mock_get_organization):
        mock_organization = Organization(name='random-name')
        mock_organization.save() # without this, the built-in database integrity test will fail since user's foreign key of organization does not exist in organization table
        mock_user_data = self.valid_data.copy()
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.data = mock_user_data
        mock_get_organization.return_value = mock_organization

        response = self.client.post(self.post_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_user_data)
    
class EventViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_url = '/eventScheduler/v1/event/post/'
        self.valid_data = {
            'name': 'random-valid-name',
            'location': 'random-valid-location',
            'description': 'random-valid-description',
            'image': 'random-image',
            'start_time': timezone.now()
        }

    @patch('eventScheduler.views.check_if_fields_are_missing')
    @patch('eventScheduler.views.EventSerializer')
    def test_post_event_success(self, mock_serializer, mock_check_if_fields_are_missing):
        mock_check_if_fields_are_missing.return_value = None
        mock_event_data = self.valid_data.copy()
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.data = mock_event_data

        response = self.client.post(self.post_url, self.valid_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_event_data)