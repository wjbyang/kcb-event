from django.conf import settings
from django.http import JsonResponse

class IncorrectUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            # Handle incorrect URL 404 responses
            if response.status_code == 404 and not request.resolver_match:
                return JsonResponse({
                    'error': 'The url you provided did not match any of the existing API endpoints. You either typed the url wrong, or your kwarg was null. The urls for this API does not always use plural nouns and does not have trailing slashes.'
                })
            return response
        except Exception as e:
            # Here you can add more sophisticated exception handling and logging
            return JsonResponse({'error': 'An unexpected server error occurred.'}, status=500)