from rest_framework import serializers
from .models.models import *

class UserSerializer(serializers.ModelSerializer):
	# organization is a model and hence is not json serializable when we return it as response in our view
	# as a result, we should turn it into json serializable format (in this case, primary key)
	organization = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = User
		fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ['guid', 'name', 'image']

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = '__all__'