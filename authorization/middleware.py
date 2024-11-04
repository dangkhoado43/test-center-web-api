from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            JWTAuthentication().authenticate(request)
        except AuthenticationFailed:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        response = self.get_response(request)
        return response

class MonitorTokenUsageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')

        logger.info(f"Request from IP: {ip_address} at {timezone.now()}")

        response = self.get_response(request)
        return response
