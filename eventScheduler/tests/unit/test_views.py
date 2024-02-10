from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from ...views import *
from ..test_data_generators.views_generator import *

class BaseViewTest(APITestCase):
    # disclaimer: most of the mocks in this file contain unrealistic data.
    def setUp(self):
        self.client = APIClient()
    
    # these generic base tests are made to work with certain patterns of models like users, events, etc.
    # we will need new base tests when we work with different types of models like ex. models that deal with entity relationships.
        
    def assert_post_status(self, mock_serializer, entity_name_singular, fail=False):
        mock_serializer.return_value.is_valid.return_value = True if not fail else False
        mock_serializer.return_value.data = 'some-entity-data' if not fail else None
        mock_serializer.return_value.save.return_value = None
        mock_serializer.return_value.errors = None if not fail else 'some-fields-are-required'
        request_data = 'some-user-data'
        post_url = f'/eventScheduler/v1/{entity_name_singular}'
        expected_status_code = status.HTTP_201_CREATED if not fail else status.HTTP_400_BAD_REQUEST
        expected_response_data = 'some-entity-data' if not fail else 'some-fields-are-required'
        response = self.client.post(post_url, request_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.data, expected_response_data)
        mock_serializer.assert_called_once_with(data=request_data)
        mock_serializer.return_value.is_valid.assert_called_once()
    
    def assert_get_status(self, entity_name_singular, mock_model, mock_serializer, fail=False):
        # the reason that get_status doesn't use one liner if/else statements for each field but instead uses a cascade is because unlike the post function that calls everything whether or not data is valid,
        # get function raises an error and should hence stop at the middle without calling some things.
        entity_guid = 'some-entity-guid'
        get_url = f'/eventScheduler/v1/{entity_name_singular}/{entity_guid}'
        if not fail:
            mock_model.get.return_value = 'some-object'
            mock_serializer.return_value.data = 'some-entity-data'
            expected_status_code = status.HTTP_200_OK
            expected_response_data = 'some-entity-data'
        else:
            mock_model.get.side_effect = User.DoesNotExist
            expected_status_code = status.HTTP_404_NOT_FOUND
            expected_response_data = {"errors": {"detail": "User not found"}}
        response = self.client.get(get_url, format='json')
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(response.status_code, expected_status_code)
        mock_model.get.assert_called_once_with(guid=entity_guid)
        if not fail:
            mock_serializer.assert_called_once_with(mock_model.get.return_value)
        else:
            mock_serializer.assert_not_called()
    
    def assert_get_all_success(self, entity_name_plural, mock_model, mock_serializer):
        # there is currently no assert_get_all_fail.
        mock_model.all.return_value = 'some-queryset-object'
        mock_serializer.return_value.data = 'some-list-of-etities'
        expected_response_data = 'some-list-of-etities'
        get_url = f'/eventScheduler/v1/{entity_name_plural}'
        response = self.client.get(get_url, format='json')
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_model.all.assert_called_once()
        mock_serializer.assert_called_once_with(mock_model.all.return_value, many=True)
    
    def assert_update_success(self, entity_name_singular, mock_model, mock_serializer):
        print()

class UserViewTest(BaseViewTest):
    def setUp(self):
        self.post_url = '/eventScheduler/v1/user'

    @patch('eventScheduler.views.UserSerializer')
    def test_post_user_success(self, mock_serializer):
        entity_name_singular = 'user'
        self.assert_post_status(mock_serializer, entity_name_singular)

    @patch('eventScheduler.views.UserSerializer')
    def test_post_user_fail(self, mock_serializer):
        entity_name_singular = 'user'
        self.assert_post_status(mock_serializer, entity_name_singular, fail=True)

class ViewUserTest(BaseViewTest):
    @patch('eventScheduler.views.UserSerializer')
    @patch('eventScheduler.views.User.objects')
    def test_get_user_success(self, mock_model, mock_serializer):
        entity_name_singular = 'user'
        self.assert_get_status(entity_name_singular, mock_model, mock_serializer)

class ViewUsersTest(BaseViewTest):
    @patch('eventScheduler.views.UserSerializer')
    @patch('eventScheduler.views.User.objects')
    def test_get_users_success(self, mock_model, mock_serializer):
        entity_name_plural = 'users'
        self.assert_get_all_success(entity_name_plural, mock_model, mock_serializer)

# class UpdateUserTest(BaseViewTest):

class EventViewTest(BaseViewTest):
    def setUp(self):
        self.post_url = '/eventScheduler/v1/event/'

    @patch('eventScheduler.views.EventSerializer')
    def test_post_event_success(self, mock_serializer):
        entity_name_singular = 'event'
        self.assert_post_status(mock_serializer, entity_name_singular)

    @patch('eventScheduler.views.EventSerializer')
    def test_post_event_fail(self, mock_serializer):
        entity_name_singular = 'event'
        self.assert_post_status(mock_serializer, entity_name_singular, fail=True)

class ViewEventTest(BaseViewTest):
    @patch('eventScheduler.views.EventSerializer')
    @patch('eventScheduler.views.Event.objects')
    def test_get_event_success(self, mock_model, mock_serializer):
        entity_name_singular = 'event'
        self.assert_get_status(entity_name_singular, mock_model, mock_serializer)

class ViewEventsTest(BaseViewTest):
    @patch('eventScheduler.views.EventSerializer')
    @patch('eventScheduler.views.Event.objects')
    def test_get_events_success(self, mock_model, mock_serializer):
        entity_name_plural = 'events'
        self.assert_get_all_success(entity_name_plural, mock_model, mock_serializer)