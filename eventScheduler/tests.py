from django.test import TestCase, Client
from eventScheduler.models import Organization
import json
import string, random

# Create your tests here.
class eventSchedulerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_organization(self):
        # test that creating a group returns status code 200
        random_group_name=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        organization_data = {
            'name': random_group_name
        }
        response = self.client.post('http://127.0.0.1:8000/eventScheduler/v1/organization/', json.dumps(organization_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        # test that creating a user returns status code 200
        first_name=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        last_name=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        org_id = '510243db-faf6-4672-a0c5-7e636f1e7eaa'
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'organization_id': org_id
        }
        response = self.client.post('http://127.0.0.1:8000/eventScheduler/v1/create_user/', json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)