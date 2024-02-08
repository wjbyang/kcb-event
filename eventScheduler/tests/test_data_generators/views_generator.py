import uuid
from django.utils import timezone

class ViewData:
    def request_format(self):
        data = dict(self.data)
        del data['guid']
        return data
    
    def server_response_format(self):
        return self.data
    
    def missing(self, *fields):
        data = dict(self.data)
        for field in fields:
            del data[field]
        return data

class UserData(ViewData):
    def __init__(self):
        self.data = {
            'guid': str(uuid.uuid4()),
            'first_name': 'random-first-name',
            'last_name': 'random-last-name',
            'email': 'random@something.com',
            'image': 'random-image-url',
            'organization_id': str(uuid.uuid4())
        }
    
class EventData(ViewData):
    def __init__(self):
        self.data = {
            'guid': str(uuid.uuid4()),
            'name': 'random-event-name',
            'location': 'random-event-location',
            'description': 'random-event-description',
            'image': 'random-image-url',
            'start_time': timezone.now().strftime("%Y-%m-%d %H:%M:%S%z")
        }
