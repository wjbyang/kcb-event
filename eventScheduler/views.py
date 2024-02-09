from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

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
		organization = Organization.objects.get(guid=self.kwargs['organization_id'])
		data = OrganizationSerializer(organization).data
		return HttpResponse(data, content_type="application/json")

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
		new_user = UserSerializer(data=request.data)
		if new_user.is_valid():
			new_user.save()
			return Response(new_user.data, status=status.HTTP_201_CREATED)
		else:
			return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

class ViewUser(APIView):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(guid=self.kwargs['user_id'])
		data = UserSerializer(user).data
		return Response(data, content_type="application/json")

class ViewUsers(APIView):
	def get(self, request, *args, **kwargs):
		users = User.objects.all()
		data = UserSerializer(users, many=True).data
		return Response(data, content_type="application/json")

class UpdateUser(APIView):
	def put(self, request, *args, **kwargs):
		user = User.objects.get(guid=self.kwargs['user_id'])
		updated_user = UserSerializer(user, data=request.data)
		if updated_user.is_valid():
			updated_user.save()
			return Response(updated_user.data, content_type="application/json")
		else:
			return Response(updated_user.errors, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")
	
class DeleteUser(APIView):
	def delete(self, request, *args, **kwargs):
		user = User.objects.get(guid=self.kwargs['user_id'])
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class EventView(APIView):
	def post(self, request, *args, **kwargs):
		new_event = EventSerializer(data=request.data)
		if new_event.is_valid():
			new_event.save()
			return Response(new_event.validated_data, status=status.HTTP_201_CREATED, content_type="application/json")
		else:
			return Response(new_event.errors, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

class ViewEvent(APIView):
	def get(self, request, *args, **kwargs):
		event = Event.objects.get(guid=self.kwargs['event_id'])
		data = EventSerializer(event).data
		return Response(data, content_type="application/json")

class ViewEvents(APIView):
	def get(self, request, *args, **kwargs):
		events = Event.objects.all()
		data = EventSerializer(events, many=True).data
		return Response(data, content_type="application/json")