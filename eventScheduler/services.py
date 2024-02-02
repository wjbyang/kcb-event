from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound

class OrganizationService:
    def get_organization_object(organization_id):
        try:
            organization = Organization.objects.get(guid=organization_id)
            return organization
        except Organization.DoesNotExist:
            return None
    def get_organization_data(organization_id):
        try:
            organization = Organization.objects.get(guid=organization_id)
            data = OrganizationSerializer(organization).data
            return data
        except Organization.DoesNotExist:
            return None