from django.conf import settings
from django.http import HttpResponseNotFound

class IncorrectUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # request.resolver_match makes sure the 404 is from bad routing
        if response.status_code == 404 and not request.resolver_match:
            return HttpResponseNotFound('Hey, did you just make an API request to the backend? Well, I have bad news for you. The url you used to make an API request didn\'t hit any routes in our server. \
Maybe you missed some "/" placements in the url. Ex. you typed "/requests" instead of "/reqests/". Maybe you got the server IP wrong. Maybe you misspelled something. Or maybe it\'s some different issue. \
Whatever it is, based on my limited experience, the issue is *most likely* in the url you used to make that API call. That\'s all I\'m saying to save you some time. But this might not always be the case. Regardless, happy debugging, my friend.')
        return response