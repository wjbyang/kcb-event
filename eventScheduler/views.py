from django.http import HttpResponse
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from eventScheduler.models import User, Organization, Group
from rest_framework import serializers

def index(request):
    return HttpResponse("Hello, world")

class OrganizationView(APIView):
	def post(self, request, *args, **kwargs):
		request = request.data
		name = request.get('name')
		newOrg = Organization(name=name)
		newOrg.save()
		return Response(newOrg.guid)

class GetOrganization(APIView):
	def get(self, request, *args, **kwargs):
		orgs = Organization.objects.all()
		data = OrganizationSerializer(orgs, many=True).data
		return Response(data, content_type="application/json")

class GetOrganizations(APIView):
	def get(self, request, *args, **kwargs):
		orgs = Organization.objects.all()
		data = OrganizationSerializer(orgs, many=True).data
		return Response(data, content_type="application/json")

class GetGroups(APIView):
	def get(self, request, *args, **kwargs):
		orgs = Group.objects.all()
		data = GroupSerializer(orgs, many=True).data
		return Response(data, content_type="application/json")

class GroupView(APIView):
	def post(self, request, *args, **kwargs):
		request = request.data
		name = request.get('name')
		existingGroup = Group.objects.filter(name=name)
		if existingGroup:
			return Response('Group already exists')
		newGroup = Group(name=name)
		newGroup.save()
		data = GroupSerializer(newGroup).data
		return Response(data, content_type="application/json")

class UserView(APIView):
    def post(self, request, *args, **kwargs):
        request_data = request.data
        first_name = request_data.get('first_name')
        last_name = request_data.get('last_name')
        organization_id = request_data.get('organization_id')
        
        organization = self.get_organization(organization_id)
        if not organization:
            return HttpResponse("organization not found", status=404, content_type='text/plain')
        
        new_user = User(first_name=first_name, last_name=last_name, organization=organization)
        new_user.save()
        
        user_data = {
            'guid': new_user.guid,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name
        }
        return Response(user_data)

    def check_if_organization_exists(self, organization_id):
        try:
            return Organization.objects.get(guid=organization_id)
        except Organization.DoesNotExist:
            return None

class ViewUser(APIView):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(guid=self.kwargs['user_id'])
		data = serialize("json", [user], fields=('first_name', 'last_name', 'organization'))
		return HttpResponse(data, content_type="application/json")

class ViewUsers(APIView):
	def get(self, request, *args, **kwargs):
		users = User.objects.all()
		data = UserSerializer(users, many=True).data
		return Response(data, content_type="application/json")

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ['guid', 'name', 'image']

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'
