from django.test import TestCase, Client
from django.urls import reverse
from eventScheduler.models import Organization
import string, random

# Create your tests here.
class eventSchedulerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_organization(self):
        # test that creating an organization with a random 5 length string name returns status code 200
        random_group_name=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        organization_data = {
            'name': random_group_name
        }
        url = reverse('organizationPost')
        response = self.client.post(url, organization_data, format="json")
        self.assertEqual(response.status_code, 200)
    
    def test_check_if_organization_exists(self):
        # first make a random organization and add it to test database
        random_group_name=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        organization_data = {
            'name': random_group_name
        }
        url = reverse('organizationPost')
        response = self.client.post(url, organization_data, format="json")
        organization_id = response.data
        
        # now fetch organization and test the actual function
        