from rest_framework import serializers
from .models import *

def validate_model_id(model, id, message):
	if not model.objects.filter(pk=id).exists():
		print("WTF")
		raise serializers.ValidationError(message)
	return id

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

	def validate_group_id(self, value):
		message = "group_id does not correspond to a valid group instance."
		return validate_model_id(Group, value, message)
	
	def validate_organization_id(self, value):
		message = "organization_id does not correspond to a valid organization instance."
		return validate_model_id(Organization, value, message)

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = '__all__'

	def validate_organization_id(self, value):
		message = "organization_id does not correspond to a valid organization instance."
		return validate_model_id(Organization, value, message)

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'
	
	def validate_organization_id(self, value):
		message = "organization_id does not correspond to a valid organization instance."
		return validate_model_id(Organization, value, message)

class UserToEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserToEvent
		fields = '__all__'

	def validate_user_id(self, value):
		message = "user_id does not correspond to a valid user instance."
		return validate_model_id(User, value, message)
	
	def validate_event_id(self, value):
		message = "event_id does not correspond to a valid event instance."
		return validate_model_id(Event, value, message)
	
	def create(self, validated_data):
		print()

class GroupToEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = GroupToEvent
		fields = '__all__'

	def validate_group_id(self, value):
		message = "group_id does not correspond to a valid group instance."
		return validate_model_id(Group, value, message)
	
	def validate_event_id(self, value):
		message = "event_id does not correspond to a valid event instance."
		return validate_model_id(Event, value, message)