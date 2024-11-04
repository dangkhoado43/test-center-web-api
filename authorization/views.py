from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Session, RevokedToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Revoke old refresh tokens
            Session.objects.filter(user=user).delete()

            # Create new tokens
            refresh = RefreshToken.for_user(user)
            ip_address = request.META.get('REMOTE_ADDR')

            # Store new refresh token in the database
            Session.objects.create(user=user, refresh_token=str(refresh), ip_address=ip_address)

            # Set HttpOnly cookie for refresh token
            response = Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
            response.set_cookie(key='refresh_token', value=str(refresh), httponly=True)

            return response
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"error": "Refresh token not found"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the refresh token is revoked
        if RevokedToken.objects.filter(token=refresh_token).exists():
            return Response({"error": "Refresh token revoked"}, status=status.HTTP_401_UNAUTHORIZED)

        # Call the parent method to perform the refresh
        response = super().post(request, *args, **kwargs)

        # Revoke the old refresh token and create a new one
        RevokedToken.objects.create(token=refresh_token)

        new_refresh = RefreshToken.for_user(request.user)
        response.set_cookie(key='refresh_token', value=str(new_refresh), httponly=True)

        return response

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        Session.objects.filter(refresh_token=refresh_token).delete()  # Remove session

        response = Response({"message": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('refresh_token')
        return response
    
class RevokeTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            RevokedToken.objects.create(token=refresh_token)
            response = Response({"message": "Token revoked"}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_token')
            return response
        return Response({"error": "No token found"}, status=status.HTTP_400_BAD_REQUEST)
