from django.test import TestCase
from django.utils import timezone # good for automatically using timezone from settings.py (UTC)
from datetime import datetime # good for working with custom timezones
from copy import deepcopy
from zoneinfo import ZoneInfo
import uuid
from ...models import *
from ...serializers import *
from ..test_data_generators.views_generator import *


"""This "unit test" is tricky because it's not really an actual "unit" test."""
"""This is because I chose not to mock models and so all of these tests have a dependency. If a serializer doesn't break but models break, then so will these tests."""
"""The reason I chose not to mock models is because that would take some time that might be better spent in other places."""
"""It's also because our models have very simple logic right now and each of them don't have complex special functions or anything. They just define fields."""
"""And thus I didn't even write any tests for models. So this test is kind of what will test both models AND serializers. But nothing else. So this is basically a sort of "twin test"."""
class BaseSerializerTest(TestCase):
    def assert_serialization_success(self, data, Model, Serializer):
        object = Model.objects.create(**data)
        serialized_object_data = Serializer(object).data
        self.assertIsNotNone(uuid.UUID(serialized_object_data.pop('guid'), version=4))
        self.assertEqual(serialized_object_data, data)
    
    def assert_deserialization_success(self, data, optional_fields, Serializer):
        deserialized_data = Serializer(data=data)
        self.assertTrue(deserialized_data.is_valid())

        for field in optional_fields:
            request_without_optional_field = deepcopy(data)
            request_without_optional_field[field] = None
            deserialized_data_without_optional_field = Serializer(data=request_without_optional_field)
            self.assertTrue(deserialized_data_without_optional_field.is_valid())
        
    def assert_deserialization_failure(self, data, required_fields, unique_non_uuid_string_fields, Model, Serializer):
        for field in required_fields:
            invalid_data = deepcopy(data)
            invalid_data[field] = None
            invalid_serialized_data = Serializer(data=invalid_data)
            self.assertFalse(invalid_serialized_data.is_valid())
            self.assertTrue(invalid_serialized_data.errors)

        # Below, we create a user, and then try to create another user with exactly the same fields. We want to test all cases where a new user is created with exactly one unique field as a duplicate.
        # The above is done by adding a string '1' to all unique fields (added at the start, since else emails will break) except one. This way we are testing one unique field at a time. 
        # It is trivial to know from the above that we can only test unique fields that are in string format and that we cannot test other data types of unique fields with this logic.
        # The provided fields should, in general, not include anything that will break if we add '1' to it, just like a uuid. 'uuid' is emphasized only to provide an easy example.
        Model.objects.create(**data)
        for i in range(len(unique_non_uuid_string_fields)):
            data_with_existing_unique_field = deepcopy(data)
            for j, field in enumerate(unique_non_uuid_string_fields):
                if i != j:
                    data_with_existing_unique_field[field] = '1' + data_with_existing_unique_field[field]
            serialized_object = Serializer(data=data_with_existing_unique_field)
            self.assertFalse(serialized_object.is_valid())

class UserSerializerTest(BaseSerializerTest):
    def setUp(self):
        self.model = User
        self.serializer = UserSerializer
        self.organization = Organization.objects.create(name='random-organization-name')
        self.data = {
            'first_name': 'random-first-name',
            'last_name': 'random-last-name',
            'email': 'random@something.com',
            'image': 'random-image-url',
            'organization_id': str(self.organization.guid)
        }

    def test_serialization(self):
        self.assert_serialization_success(self.data, self.model, self.serializer)
        
    def test_deserialization(self):
        optional_fields = ['image']
        required_fields = ['first_name', 'last_name', 'email', 'organization_id']
        unique_non_uuid_string_fields = ['email']
        self.assert_deserialization_success(self.data, optional_fields, self.serializer)
        self.assert_deserialization_failure(self.data, required_fields, unique_non_uuid_string_fields, self.model, self.serializer)
        
class EventSerializerTest(BaseSerializerTest):
    def setUp(self):
        self.model = Event
        self.serializer = EventSerializer
        self.data = EventData(current_time=True).request_format()

    def test_serialization(self):
        self.assert_serialization_success(self.data, self.model, self.serializer)
    
    def test_timezone_serialization(self):
        data_with_different_timezone = deepcopy(self.data)
        ny_tz = ZoneInfo('America/New_York')
        ny_time = datetime.now(ny_tz)
        data_with_different_timezone['start_time'] = ny_time
        event = Event.objects.create(**data_with_different_timezone)
        serialized_event_time = EventSerializer(event).data['start_time']
        datetime.fromisoformat(serialized_event_time) # if there is no error here, test passes
        
    def test_deserialization(self):
        optional_fields = ['image']
        required_fields = ['name', 'location', 'description', 'start_time']
        unique_non_uuid_string_fields = []
        self.assert_deserialization_success(self.data, optional_fields, self.serializer)
        self.assert_deserialization_failure(self.data, required_fields, unique_non_uuid_string_fields, self.model, self.serializer)