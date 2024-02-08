from django.test import TestCase
from ...models import *
from ...serializers import *
from ..test_data_generators.views_generator import *
import uuid
from copy import deepcopy

class UserSerializerTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='random-organization-name')
        self.data = {
            'first_name': 'random-first-name',
            'last_name': 'random-last-name',
            'email': 'random@something.com',
            'image': 'random-image-url',
            'organization_id': str(self.organization.guid)
        }

    def test_serialization_success(self):
        user = User.objects.create(**self.data)
        serialized_user_data = UserSerializer(user).data
        # I want to conveniently use self.data to assert the serialized data.
        # Therefore, I check the validity of guid separately and then delete it from serialized data.
        self.assertIsNotNone(uuid.UUID(serialized_user_data.pop('guid'), version=4))
        self.assertEqual(serialized_user_data, self.data)
        
    def test_deserialization_success(self):
        request_without_image = deepcopy(self.data)
        request_without_image['image'] = None
        user = UserSerializer(data=self.data)
        user_without_image = UserSerializer(data=request_without_image)
        self.assertTrue(user.is_valid())
        self.assertTrue(user_without_image.is_valid())

    def test_deserialization_failure(self):
        # test missing fields
        user1, user2, user3, user4, user5 = deepcopy(self.data), deepcopy(self.data), deepcopy(self.data), deepcopy(self.data), deepcopy(self.data)
        user1['first_name'], user2['last_name'], user3['email'], user4['organization_id'] =  None, None, None, None
        for user in [user1, user2, user3, user4]:
            serialized_user = UserSerializer(data=user)
            self.assertFalse(serialized_user.is_valid())
            self.assertTrue(serialized_user.errors)

        # test a case where someone registers with same email as existing one
        User.objects.create(**self.data)
        serialized_user = UserSerializer(data=user5)
        self.assertFalse(serialized_user.is_valid())
        
class EventSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'name': 'random-event-name',
            'last_name': 'random-last-name',
            'email': 'random@something.com',
            'image': 'random-image-url',
            'organization_id': str(self.organization.guid)
        }

    def test_serialization_success(self):
        user = User.objects.create(**self.data)
        serialized_user_data = UserSerializer(user).data
        # I want to conveniently use self.data to assert the serialized data.
        # Therefore, I check the validity of guid separately and then delete it from serialized data.
        self.assertIsNotNone(uuid.UUID(serialized_user_data.pop('guid'), version=4))
        self.assertEqual(serialized_user_data, self.data)
        
    def test_deserialization_success(self):
        request_without_image = deepcopy(self.data)
        request_without_image['image'] = None
        user = UserSerializer(data=self.data)
        user_without_image = UserSerializer(data=request_without_image)
        self.assertTrue(user.is_valid())
        self.assertTrue(user_without_image.is_valid())

    def test_deserialization_failure(self):
        # test missing fields
        user1, user2, user3, user4, user5 = deepcopy(self.data), deepcopy(self.data), deepcopy(self.data), deepcopy(self.data), deepcopy(self.data)
        user1['first_name'], user2['last_name'], user3['email'], user4['organization_id'] =  None, None, None, None
        for user in [user1, user2, user3, user4]:
            serialized_user = UserSerializer(data=user)
            self.assertFalse(serialized_user.is_valid())
            self.assertTrue(serialized_user.errors)

        # test a case where someone registers with same email as existing one
        User.objects.create(**self.data)
        serialized_user = UserSerializer(data=user5)
        self.assertFalse(serialized_user.is_valid())
        