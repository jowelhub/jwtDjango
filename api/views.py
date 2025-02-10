from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, FrontendJWTSerializer

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FrontendJWTSerializer(data=request.data)
        if serializer.is_valid():
            frontend_token = serializer.validated_data['token']
            try:
                # Decode with verification
                payload = jwt.decode(frontend_token, settings.JWT_DECODE_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({"detail": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.InvalidTokenError:
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            email = payload.get('email')
            name = payload.get('name')
            profile_image = payload.get('picture') or payload.get('profile_image')

            if not email or not name:
                return Response({"detail": "Token missing required user info."}, status=status.HTTP_400_BAD_REQUEST)

            user, created = User.objects.get_or_create(email=email, defaults={'name': name, 'profile_image': profile_image})
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FrontendJWTSerializer(data=request.data)
        if serializer.is_valid():
            frontend_token = serializer.validated_data['token']
            try:
                payload = jwt.decode(frontend_token, settings.JWT_DECODE_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({"detail": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.InvalidTokenError:
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            email = payload.get('email')
            if not email:
                return Response({"detail": "Token missing email."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found. Please register."}, status=status.HTTP_404_NOT_FOUND)

            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
