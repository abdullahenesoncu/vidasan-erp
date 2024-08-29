from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer
from django.contrib.auth import get_user_model
from backend.settings import GOOGLE_USERINFO_URL
from django.utils import timezone
from datetime import timedelta
from .helpers import get_random_string, IsUserVerified
import requests
from allauth.account.adapter import get_adapter
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import User, UserType
from .serializers import UserSerializerPublic
from .helpers import IsUserVerified
from LoggingApp import logger

User = get_user_model()

class SignupView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
      
      return Response(UserSerializer( user ).data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
   """
   API view for user login.
   """
   serializer_class = LoginSerializer
   permission_classes = [AllowAny]

   def post(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      token, _ = Token.objects.get_or_create(user=user)
      user.token = str(token)
      user.save()
      return Response(UserSerializer( user ).data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    permission_classes = [IsUserVerified]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = request.user
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully.'})
        return Response(serializer.errors, status=400)

def get_user_info_from_google_token(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    return response.json()

def create_or_get_user_with_google_data(access_token):
    data = get_user_info_from_google_token(access_token)
    if data:
        try:
            email = data.get('email')
            first_name = data.get('given_name', '')
            last_name = data.get('family_name', '')
            name = data.get('name', first_name + ' ' + last_name)
            email_verified = data.get('email_verified', True)
            
            user = User.objects.filter(email=email).first()
            if user:
                return user

            return User.objects.create(
                username=email.split('@')[0]+get_random_string(12),
                email=email,
                first_name=first_name,
                last_name=last_name,
                name=name,
                email_verified=email_verified
            )
        except Exception as e:
            print(e)
            pass
    return None

class GoogleLoginView(APIView):
   permission_classes = [AllowAny]
   def get(self, request):
      access_token = request.GET.get('code') or request.data.get('code')
      if access_token:
         try:
            user = create_or_get_user_with_google_data(access_token)
            token, _ = Token.objects.get_or_create(user=user)
            user.token = str(token)
            user.save()
            return Response(UserSerializer( user ).data, status=status.HTTP_200_OK)
         except Exception as e:
             print(e)
             pass

      return Response({}, status.HTTP_400_BAD_REQUEST)

class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        email = request.GET.get('email') or request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({}, status.HTTP_400_BAD_REQUEST)
        user.reset_password_token = get_random_string()
        user.reset_password_expiration = timezone.now() + timedelta(minutes=3)
        user.save()
        adapter = get_adapter()
        adapter.send_password_reset_mail(request, user)
        return Response(ResetPasswordRequestSerializer(user).data, status=status.HTTP_200_OK)

class ResetPasswordView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      user.set_password(serializer.validated_data['password'])
      user.reset_password_token = None
      user.reset_password_expiration = None
      user.save()
      
      return Response(UserSerializer( user ).data, status=status.HTTP_200_OK)

class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsUserVerified]

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        logger.debug(f'User {self.request.user} is requesting serializer for User, user type: {user_type}')
        if user_type in [UserType.ADMIN, UserType.PLANLAMA]:
            return UserSerializer
        else:
            return UserSerializerPublic

    def get_queryset(self):
        if self.get_serializer_class() == UserSerializerPublic:
            return User.objects.filter(email=self.request.user.email).all()
        else:
            return User.objects.filter(is_superuser=False)

    def list(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is listing User objects')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if self.get_serializer_class() == UserSerializerPublic:
            logger.critical(f'{self.request.user} tried to create User without permission')
            raise PermissionDenied("You do not have permission to create this object.")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'User {self.request.user} created a new User: ID={serializer.data["id"]}, Email={serializer.data["email"]}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f'Failed to create User, errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUserVerified]

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        logger.debug(f'User {self.request.user} is requesting serializer for User, user type: {user_type}')
        if user_type in [UserType.ADMIN, UserType.PLANLAMA]:
            return UserSerializer
        else:
            return UserSerializerPublic

    def get_queryset(self):
        if self.get_serializer_class() == UserSerializerPublic:
            return User.objects.filter(email=self.request.user.email)
        else:
            return User.objects.filter(is_superuser=False)

    def get(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is retrieving User object with ID={kwargs.get("pk")}')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        if self.get_serializer_class() == UserSerializerPublic:
            logger.critical(f'{self.request.user} tried to update User without permission: ID={user.id}, Email={user.email}')
            raise PermissionDenied("You do not have permission to update this object.")

        logger.info(f'User {self.request.user} is updating User: ID={user.id}, Email={user.email}')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if self.get_serializer_class() == UserSerializerPublic:
            logger.critical(f'{self.request.user} tried to delete User without permission: ID={user.id}, Email={user.email}')
            raise PermissionDenied("You do not have permission to delete this object.")

        logger.info(f'User {self.request.user} is deleting User: ID={user.id}, Email={user.email}')
        return self.destroy(request, *args, **kwargs)