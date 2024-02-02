from django.test import TestCase
from ...models import *
from ...services import *

class OrganizationServiceTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='random-valid-organization-name')
        self.organization_data = OrganizationSerializer(self.organization).data
    def test_get_organization_success(self):
        organizaiton_guid = self.organization.guid
        organization_object = OrganizationService.get_organization_object(organizaiton_guid)
        organization_data = OrganizationService.get_organization_data(organizaiton_guid)
        self.assertEqual(organization_object, self.organization)
        self.assertEqual(organization_data, self.organization_data)
    def test_get_organization_fail(self):
        organizaiton_guid = Organization(name='random-false-organization-name').guid
        organization_object = OrganizationService.get_organization_object(organizaiton_guid)
        organization_data = OrganizationService.get_organization_data(organizaiton_guid)
        self.assertEqual(organization_object, None)
        self.assertEqual(organization_data, None)