from .models.models import *
from .serializers import *
from rest_framework.exceptions import NotFound

def get_organization_data(organization_id):
    try:
        organization = Organization.objects.get(guid=organization_id)
        data = OrganizationSerializer(organization).data
        return data
    except Organization.DoesNotExist:
        raise NotFound('organization not found')