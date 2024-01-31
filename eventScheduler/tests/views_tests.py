from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from eventScheduler.models.models import *
from eventScheduler.views import *

# Create your tests here.
class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_url = 'v1/user/post/'
        self.valid_data = {
            'first_name': 'random-valid-first-name',
            'last_name': 'random-valid-last-name',
            'organization_id': 'random-valid-organization-id'
        }

    @patch('eventScheduler.views.get_organization_data')
    @patch('eventScheduler.views.UserSerializer')
    # function parameter of mocks need to be reverse order of patch declarations. Uhm... django, WHY? 
    def test_post_user_success(self, mock_serializer, mock_get_organization):
        # set up mocks
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.data = mock_user_data
        mock_organization = Organization(name='random-name')
        mock_get_organization.return_value = mock_organization
        mock_user_data = {'first_name': 'random-valid-first-name', 'last_name': 'random-valid-last-name', 'organization': mock_organization}
        response = self.client.post(self.post_url, self.valid_data, format='json')
        self.assertEqual(response.data, mock_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)