from django.db import models
import uuid

# KCB
class Organization(models.Model):
	guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	name = models.CharField(max_length=100)
	image = models.TextField()

# YA1, YA2, etc
class Group(models.Model):
	guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	name = models.CharField(max_length=100)

class User(models.Model):
	guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	image = models.TextField()
	deleted = models.BooleanField(default=False)
	isAdmin = models.BooleanField(default=False)
	organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.PROTECT)

class Event(models.Model):
	guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	name = models.TextField()
	location = models.CharField(max_length=50)
	description = models.TextField()
	image = models.TextField()
	start_time = models.DateTimeField()
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField()
	deleted = models.BooleanField(default=False)
