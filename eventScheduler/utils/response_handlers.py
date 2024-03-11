from rest_framework.response import Response

class SuccessResponseHandler:
    @staticmethod
    def handle(data, status_code, message="Success"):
        return Response({
            'status': 'success',
            'message': message,
            'data': data
        }, status=status_code, content_type='application/json')

class ErrorResponseHandler:
    @staticmethod
    def handle(message, status_code):
        return Response({
            'status': 'error',
            'message': message,
            'data': None
        }, status=status_code, content_type='application/json')
