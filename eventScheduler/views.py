from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .utils.response_handlers import *

class KcbResponse(Response):
	def __init__(self, *args, **kwargs):
		self.message = kwargs.pop("message") if "message" in kwargs.keys() else ""
		self.results = kwargs.pop("results") if "results" in kwargs.keys() else []
		kwargs["data"] = {"message": self.message, "results": self.results}
		super().__init__(*args, **kwargs)

class BaseView(APIView):
	def post_data(self, data, Serializer):
		try:
			serializer = Serializer(data=data)
			if not serializer.is_valid():
				return ErrorResponseHandler.handle(message=str(serializer.errors), status_code=status.HTTP_400_BAD_REQUEST)
			serializer.save()
			return SuccessResponseHandler.handle(data=serializer.data, status_code=status.HTTP_201_CREATED)
		except Exception as e:
			return ErrorResponseHandler.handle(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
	
	def get_object(self, guid, Model, Serializer, name):
		try:
			object = Model.objects.get(guid=guid)
			data = Serializer(object).data
		except Model.DoesNotExist:
			return ErrorResponseHandler.handle(message=f"{name} not found.", status_code=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return ErrorResponseHandler.handle(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return SuccessResponseHandler.handle(data=data, status_code=status.HTTP_200_OK)
	
	def get_objects(self, Model, Serializer):
		try:
			objects = Model.objects.all()
			data = Serializer(objects, many=True).data
			status_code=status.HTTP_200_OK
			return SuccessResponseHandler.handle(data, status_code)
		except Exception as e:
			return ErrorResponseHandler.handle(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrganizationView(BaseView):
	def post(self, request, *args, **kwargs):
		return self.post_data(data=request.data, Serializer=OrganizationSerializer)

class ViewOrganization(BaseView):
	def get(self, request, *args, **kwargs):
		return self.get_object(guid=self.kwargs['organization_id'], Model=Organization, Serializer=OrganizationSerializer, name="Organization")

class ViewOrganizations(BaseView):
	def get(self, request, *args, **kwargs):
		return self.get_objects(Model=Organization, Serializer=OrganizationSerializer)
	
class GroupView(BaseView):
	def post(self, request, *args, **kwargs):
		return self.post_data(data=request.data, Serializer=GroupSerializer)

class ViewGroup(BaseView):
	def get(self, request, *args, **kwargs):
		return self.get_object(guid=self.kwargs['group_id'], Model=Group, Serializer=GroupSerializer, name="Group")

class ViewGroups(BaseView):
	def get(self, request, *args, **kwargs):
		return self.get_objects(Model=Group, Serializer=GroupSerializer)

class UserView(BaseView):
	def post(self, request, *args, **kwargs):
		return self.post_data(data=request.data, Serializer=UserSerializer)

class ViewUser(BaseView):
	def get(self, request, *args, **kwargs):
		return self.get_object(guid=self.kwargs['user_id'], Model=User, Serializer=UserSerializer, name="User")

class ViewUsers(BaseView):
	def get(self, request, *args, **kwargs):
		return self.get_objects(Model=User, Serializer=UserSerializer)

class UpdateUser(BaseView):
	def put(self, request, *args, **kwargs):
		try:
			user = User.objects.get(guid=self.kwargs['user_id'])
		except User.DoesNotExist:
			return Response({"errors": {"detail": "User not found"}}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
		updated_user = UserSerializer(user, data=request.data)
		if updated_user.is_valid():
			updated_user.save()
			return Response(updated_user.data, content_type='application/json')
		else:
			return Response(updated_user.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
	
class DeleteUser(BaseView):
	def delete(self, request, *args, **kwargs):
		try:
			user = User.objects.get(guid=self.kwargs['user_id'])
		except User.DoesNotExist:
			return Response({"errors": {"detail": "User not found"}}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class EventView(BaseView):
	def post(self, request, *args, **kwargs):
		return self.post_data(data=request.data, Serializer=EventSerializer)

class ViewEvent(BaseView):
	def get(self, request, *args, **kwargs):
		return self.get_object(guid=self.kwargs['event_id'], Model=Event, Serializer=EventSerializer, name="Event")

class ViewEvents(BaseView):
	def get(self, request, *args, **kwargs):
		return self.get_objects(Model=Event, Serializer=EventSerializer)

class UpdateEvent(BaseView):
	def put(self, request, *args, **kwargs):
		try:
			event = Event.objects.get(guid=self.kwargs['event_id'])
		except Event.DoesNotExist:
			return Response({"errors": {"detail": "Event not found"}}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
		updated_event = EventSerializer(event, data=request.data)
		if updated_event.is_valid():
			updated_event.save()
			return Response(updated_event.data, content_type='application/json')
		else:
			return Response(updated_event.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
	
class DeleteEvent(BaseView):
	def delete(self, request, *args, **kwargs):
		try:
			event = Event.objects.get(guid=self.kwargs['event_id'])
		except Event.DoesNotExist:
			return Response({"errors": {"detail": "Event not found"}}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
		event.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class EventAttending(BaseView):
	def post(self, request, *args, **kwargs):
		return self.post_data(data=request.data, Serializer=UserToEventSerializer)