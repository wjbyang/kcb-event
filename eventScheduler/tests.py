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
        print(response)
        self.assertEqual(response.status_code, 200)