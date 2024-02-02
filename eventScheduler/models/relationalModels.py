from django.db import models
from .models import *

class UserToEvent(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	event = models.ForeignKey(Event, on_delete=models.PROTECT)
	attending = models.BooleanField(default=False)

class GroupToEvent(models.Model):
	group = models.ForeignKey(Group, on_delete=models.PROTECT)
	event = models.ForeignKey(Event, on_delete=models.PROTECT)
	hosting = models.BooleanField(default=False)