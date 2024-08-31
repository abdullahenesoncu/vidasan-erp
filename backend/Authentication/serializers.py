from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.utils import timezone
from .helpers import get_random_string

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
   """
   Serializer for user signup.
   """
   email = serializers.EmailField(
      required=True,
      validators=[UniqueValidator(queryset=User.objects.all())]
   )
   name = serializers.CharField(required=True)
   password = serializers.CharField(write_only=True)

   def create(self, validated_data):
      user = User.objects.create_user(
         username=get_random_string(),
         name=validated_data['name'],
         email=validated_data['email'],
         password=validated_data['password'],
      )
      return user
   
   class Meta:
      model = User
      fields = ('email', 'name', 'password')


class LoginSerializer(serializers.Serializer):
   """
   Serializer for user login.
   """
   email = serializers.EmailField(required=True)
   password = serializers.CharField(required=True)

   def validate(self, attrs):
      email = attrs.get('email')
      password = attrs.get('password')
   
      user = User.objects.filter(email=email).first()
      if user and user.check_password(password):
         if not user.is_active:
               raise serializers.ValidationError('User account is disabled.')
         attrs['user'] = user
         return attrs
      raise serializers.ValidationError('Invalid email or password.')
   
   class Meta:
      model = User
      fields = ('email', 'password')

class UserSerializer(serializers.ModelSerializer):
   id = serializers.IntegerField()
   name = serializers.CharField()
   email = serializers.EmailField()
   password = serializers.CharField(write_only=True)
   user_verified = serializers.BooleanField()
   token = serializers.CharField()
   user_type = serializers.CharField()
   
   class Meta:
      model = User
      fields = ('id', 'email', 'name', 'password', 'user_verified', 'token', 'user_type', 'is_active')
      write_only_fields = ['password']

class UserSerializerPublic(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ( 'id', 'email', 'name' )
      read_only_fields = fields

class ResetPasswordRequestSerializer(serializers.Serializer):
   email = serializers.EmailField(required=True)
   reset_password_expiration = serializers.DateTimeField(required=True)

   class Meta:
      model = User
      fields = ('email', 'reset_password_expiration')

class ResetPasswordSerializer(serializers.ModelSerializer):
   token = serializers.CharField(required=True)
   password = serializers.CharField(required=True, write_only=True)

   def validate(self, attrs):
      email = attrs.get('email')
      token = attrs.get('token')

      user = User.objects.filter(reset_password_token=token).first()

      if not user:
         raise serializers.ValidationError('Invalid email')
      
      if not user.reset_password_token:
         raise serializers.ValidationError('Invalid token')
      
      if user.reset_password_expiration < timezone.now():
         raise serializers.ValidationError('Token expired')

      attrs['user'] = user
      return attrs
   
   class Meta:
      model = User
      fields = ('token', 'password')
   
