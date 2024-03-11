
from .models import *

class EventResponse:
	def __init__(self, event: Event, attendingCount):
		guid = event.guid
		name = event.name
		description = event.description
		image = event.image
		startTime = event.startTime
		attendingCount = attendingCount

class EventService:
	def __init__(self):
		pass

	def fetch_all_events_for_user(self, userId):
		user = User.objects.get(guid=userId)
		group = user.group

		userToEventAttendingOnly = UserToEvent.objects.filter(user = user.guid, attending = True).all()
		groupToEvent = GroupToEvent.objects.get(group = group.guid)

		for event in groupToEvent:
			# check if guest has selected attendance
			eventResponse = EventResponse








