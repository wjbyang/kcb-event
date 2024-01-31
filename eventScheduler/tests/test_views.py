from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from ..models.models import *
from ..views import *

class UserViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_url = '/eventScheduler/v1/user/post/'
        self.valid_data = {
            'first_name': 'random-valid-first-name',
            'last_name': 'random-valid-last-name',
            'email': 'random-email',
            'organization_id': 'random-valid-organization-id'
        }

    @patch('eventScheduler.views.get_organization_data')
    @patch('eventScheduler.views.UserSerializer')
    def test_post_user_success(self, mock_serializer, mock_get_organization):
        mock_organization = Organization(name='random-name')
        mock_organization.save() # without this, the built-in database integrity test will fail since user's foreign key of organization does not exist in organization table
        mock_user_data = {'first_name': 'random-valid-first-name', 'last_name': 'random-valid-last-name', 'email': 'random-email', 'organization': 'random-organization-id'}
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.data = mock_user_data
        mock_get_organization.return_value = mock_organization

        response = self.client.post(self.post_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_user_data)
    