from django.db import models
import uuid

# KCB
class Organization(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    image = models.TextField(null=True, blank=True)

# YA1, YA2, etc
class Group(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    image = models.TextField(null=True, blank=True)
    organization_id = models.ForeignKey(Organization, on_delete=models.PROTECT)

class User(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    image = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    group_id = models.ForeignKey(Group, on_delete=models.PROTECT)
    organization_id = models.ForeignKey(Organization, on_delete=models.PROTECT)

class Event(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField()
    location = models.CharField(max_length=50)
    description = models.TextField()
    image = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    organization_id = models.ForeignKey(Organization, on_delete=models.PROTECT)

# relational models
    
class UserToEvent(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    event_id = models.ForeignKey(Event, on_delete=models.PROTECT)
    attending = models.BooleanField(default=False)

class GroupToEvent(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.PROTECT)
    event_id = models.ForeignKey(Event, on_delete=models.PROTECT)
    hosting = models.BooleanField(default=False)