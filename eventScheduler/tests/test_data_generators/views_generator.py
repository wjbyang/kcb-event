import uuid
from django.utils import timezone

class ViewData:
    def request_format(self):
        # most requests here don't contain guid in JSON data, but rather in URL arguments during put requests
        data = dict(self.data)
        del data['guid']
        return data
    
    def server_response_format(self):
        # server responses do contain guid data
        return self.data
    
    def missing(self, *fields):
        data = dict(self.data)
        for field in fields:
            del data[field]
        return data

class UserData(ViewData):
    def __init__(self, *, random_ids=False, random_guid=False, random_org_id=False):
        self.data = {
            'guid': str(uuid.uuid4()) if (random_ids or random_guid) else '3c2b7342-6b2d-4da9-9920-36613406c14e',
            'first_name': 'random-first-name',
            'last_name': 'random-last-name',
            'email': 'random@something.com',
            'image': 'random-image-url',
            'organization_id': str(uuid.uuid4()) if random_org_id else 'd659d324-cf7a-47e1-966f-91efdb24b803'
        }
    
class EventData(ViewData):
    def __init__(self, *, random_ids=False, random_guid=False, current_time=False):
        self.data = {
            'guid': str(uuid.uuid4()) if (random_ids or random_guid) else '010fb433-afc1-4037-9d24-fa1627e13f4a',
            'name': 'random-event-name',
            'location': 'random-event-location',
            'description': 'random-event-description',
            'image': 'random-image-url',
            'start_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S%z') if current_time else '2024-02-09 06:10:24+0000' 
        }
