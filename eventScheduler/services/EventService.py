
from .models import *

class UserEventResponse:
	def __init__(self, event: Event, userAttendance: bool):
		guid = event.guid
		name = event.name
		description = event.description
		image = event.image
		startTime = event.startTime
		attendingCount = event.attendingCount

class EventDetailsUserResponse:
	def __init__(self, user: User, attending: bool):
		guid = user.guid
		first_name = user.first_name
		last_name = user.last_name
		image = user.image
		attending = attending

class EventDetailsResponse:
	def __init__(self, event: Event, attendingUsers: list(EventDetailsUserResponse)):
		guid = event.guid
		name = event.name
		description = event.description
		image = event.image
		startTime = event.startTime
		attendingCount = event.attendingCount
		attendingUsers = attendingUsers

class EventService:
	def __init__(self):
		pass

	def fetch_all_events_for_user(self, userId) -> list(UserEventResponse):
		user = User.objects.get(guid=userId)
		group = user.group

		# fetch all events that this group is part of (hosting or not)
		groupEvents = GroupToEvent.objects.get(group = group.guid)

		# get each event data
		eventIds = [event.guid for event in groupEvents]
		eventsData = Events.objects.filter(guid__in = eventIds).value()

		# get user's attending events
		userAttendingEvents = UserToEvent.objects.filter(user = user.guid, attending = True).value()

		userEventResponses = []
		for event in groupEvents:
			# check if guest has selected attendance
			userAttending = True if any([attendingEvent.guid == event.guid for attendingEvent in userAttendingEvents]) else False
			userEventResponse = UserEventResponse(event, userAttending)
			userEventResponses.append(userEventResponse)
		return userEventResponses

	def fetch_specific_event_details(self, userId, eventId) -> EventResponse:
		user = User.objects.get(guid=userId)
		event = Event.objects.get(guid = eventId)

		eventUserResponses = UserToEvent.objects.filter(event_id = eventId).values()
		userIds = [userToEvent.user_id for userToEvent in eventUserResponses]

		userDataMap = {user.guid: user for user in User.objects.filter(guid__in=userIds).values()}
		userResponses = []
		for eventUser in eventUserResponses:
			userData = userDataMap[eventUser.user_id]
			response = EventDetailsUserResponse(userData, eventUser.attending)
			userResponses.append(response)

		return EventDetailsResponse(event, userResponses)

	def update_user_event_attendance(self, userId, eventId, newAttendanceState):
		'''
			1. update users attendance state
			2. update event's attendance count

			WORK IN PROGRESS
		'''
		user = User.objects.get(guid=userId)
		event = Event.objects.get(guid=eventId)
		groupEvent = GroupToEvent.objects.filter(event_id = eventId, group_id = user.group_id)
		if groupEvent.isEmpty():
			return # throw an error or something for views.py to return to client

		# fetch for userToEvent, if it doesnt exist, create a new one
		userToEvent = UserToEvent.objects.filter(user_id = userId, event_id = eventId).value()


