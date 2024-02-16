from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    organization_id = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    organization_id = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Group
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    organization_id = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Event
        fields = '__all__'

class UserToEventSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = UserToEvent
        fields = '__all__'

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        event_id = validated_data.get('event_id')
        attending = validated_data.get('attending')
        user_to_event_instance, created = UserToEvent.objects.update_or_create(
            user_id=user_id,
            event_id=event_id,
            defaults={'attending': attending}
        )
        return user_to_event_instance

class GroupToEventSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = GroupToEvent
        fields = '__all__'