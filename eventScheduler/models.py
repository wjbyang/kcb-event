from django.db import models
import uuid

# Create your models here.
class Organization(models.Model):
	guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	name = models.CharField(max_length=100)
	image = models.TextField()

class Group(models.Model):
	guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	name = models.CharField(max_length=100)

class Event(models.Model):
	guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	name = models.TextField()
	location = models.CharField(max_length=50)
	description = models.TextField()
	image = models.TextField()
	startTime = models.DateTimeField()
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField()
	deleted = models.BooleanField(default=False)

class User(models.Model):
	guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	firstName = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	email = models.EmailField()
	image = models.TextField()
	deleted = models.BooleanField(default=False)
	organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

class UserToEvent(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	event = models.ForeignKey(Event, on_delete=models.PROTECT)
	attending = models.BooleanField(default=False)


# class UserInGroup(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.PROTECT)
# 	group = models.ForeignKey(Group, on_delete=models.PROTECT)
