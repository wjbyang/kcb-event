from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class IncorrectUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Handle incorrect URL 404 responses
        if response.status_code == 404 and not request.resolver_match:
            return Response({
                'status': 'error',
                'message': 'The url you provided did not match any of the existing API endpoints. You either typed the url wrong, or your kwarg was null. The urls for this API does not always use plural nouns and does not have trailing slashes.',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        return response