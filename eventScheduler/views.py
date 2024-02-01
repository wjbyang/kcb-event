from django.http import HttpResponse
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models.models import *
from .serializers import *
from .services import *
from .utility import *

def index(request):
	return HttpResponse("Hello, world")

class OrganizationView(APIView):
	def post(self, request, *args, **kwargs):
		request = request.data
		name = request.get('name')
		new_organization = Organization(name=name)
		new_organization.save()
		data = OrganizationSerializer(new_organization).data
		return Response(data, content_type="application/json")

class ViewOrganization(APIView):
	def get(self, request, *args, **kwargs):
		return get_organization_data(kwargs['organization_id'])

class ViewOrganizations(APIView):
	def get(self, request, *args, **kwargs):
		orgs = Organization.objects.all()
		data = OrganizationSerializer(orgs, many=True).data
		return Response(data, content_type="application/json")

class ViewGroups(APIView):
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
		required_fields = ['first_name', 'last_name', 'email', 'organization_id']
		check_if_fields_are_missing(request_data,required_fields)
		first_name = request_data.get('first_name')
		last_name = request_data.get('last_name')
		email = request_data.get('email')
		organization_id = request_data.get('organization_id')
		# if get_organization_data raises an exception, it will propagate up and terminate the post request
		organization = get_organization_data(organization_id)
		new_user = User(first_name=first_name, last_name=last_name, email=email, organization=organization)
		new_user.save()
		data = UserSerializer(new_user).data
		return Response(data)

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

class EventView(APIView):
	def post(self, request, *args, **kwargs):
		request_data = request.data
		required_fields = ['name', 'location', 'description', 'start_time']
		check_if_fields_are_missing(request_data,required_fields)
		name = request_data.get('name')
		location = request_data.get('location')
		description = request_data.get('description')
		image = request_data.get('image')
		start_time = request.data.get('start_time')
		new_event = Event(name=name, location=location, description=description, image=image, start_time=start_time)
		new_event.save()
		data = EventSerializer(new_event).data
		return Response(data)

class ViewEvent(APIView):
	def get(self, request, *args, **kwargs):
		event = User.objects.get(guid=self.kwargs['event_id'])
		data = EventSerializer(event).data
		return HttpResponse(data, content_type="application/json")

class ViewEvents(APIView):
	def get(self, request, *args, **kwargs):
		events = Event.objects.all()
		data = EventSerializer(events, many=True).data
		return Response(data, content_type="application/json")