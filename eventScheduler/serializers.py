from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
	organization_id = serializers.UUIDField(write_only=True, required=True)
	
	class Meta:
		model = User
		fields = ['guid', 'first_name', 'last_name', 'email', 'image', 'organization_id']

	def create(self, validated_data):
		organization_id = validated_data.pop('organization_id')
		if not organization_id:
			raise serializers.ValidationError({'organization_id': 'This field is required.'})
		try: 
			organization = Organization.objects.get(guid=organization_id)
		except Organization.DoesNotExist:
			raise serializers.ValidationError({'organization_id': 'Invalid organization_id or Organization does not exist.'})
		organization = Organization.objects.get(guid=organization_id)
		validated_data['organization'] = organization
		return super(UserSerializer, self).create(validated_data)

	def to_representation(self, instance):
		representation = super(UserSerializer, self).to_representation(instance)
		representation['organization_id'] = str(instance.organization.guid) if instance.organization else None
		return representation

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ['guid', 'name', 'image']

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ['guid', 'name']

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['guid', 'name', 'location', 'description', 'image', 'start_time']