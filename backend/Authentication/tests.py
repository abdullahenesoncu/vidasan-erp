from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.test import RequestFactory
from allauth.socialaccount.models import SocialApp
from backend.settings import GOOGLE_CREDENTIALS
from django.utils import timezone, dateparse

User = get_user_model()

class TestUser:
   def __init__(self, name=None, password=None, email=None, access_token=None):
      self.name = name or 'Test User'
      self.password = password or 'testpassword'
      self.email = email or 'testuser@test.com'
      self.access_token = access_token or '23r2kmroij233o13joml1'
      self.token = None
   
   @property
   def id(self):
      return User.objects.get(email=self.email).id

class AuthenticationTestBase(APITestCase):

   def setUp(self):
      self.signup_url = reverse('auth_signup')
      self.login_url = reverse('auth_login')
      self.change_password_url = reverse('auth_change_password')
      self.logout_url = reverse('auth_logout')
      self.reset_password_request_url = reverse('auth_reset_password_request')
      self.reset_password_url = reverse('auth_reset_password')
      self.google_login_url = reverse('auth_google_login')
      self.logout_url = reverse('auth_logout')
      self.factory = RequestFactory()
   
   def signup(self, testUser):
      usersCount = User.objects.count()
      data = {
         'name': testUser.name,
         'email': testUser.email,
         'password': testUser.password,
      }
      response = self.client.post( self.signup_url, data, format='json' )
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(User.objects.count(), usersCount + 1)
      self.assertEqual(User.objects.get(email=testUser.email).name, testUser.name)

   def verify_email(self, testUser):
      User.objects.filter(email=testUser.email).update(email_verified=True)
   
   def login(self, testUser):
      data = {
         'email': testUser.email,
         'password': testUser.password,
      }
       
      response = self.client.post(self.login_url, data, format='json')
      
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertIn('token', response.data)
      testUser.token = response.data['token']
   
   def changePassword(self, testUser):
      data = {
         'id': 1,
         'new_password': 'newtestpassword'
      }
      headers = {'HTTP_AUTHORIZATION': f'Token {testUser.token}'}
      response = self.client.put(self.change_password_url, data, format='json', **headers)
      
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(User.objects.get(email=testUser.email).check_password('newtestpassword'), True)
      
      testUser.password = 'newtestpassword'
   
   def logout(self, testUser):
      headers = {'HTTP_AUTHORIZATION': f'Token {testUser.token}'}
      response = self.client.post(self.logout_url, **headers)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(Token.objects.count(), 0)
      testUser.token = None

   def reset_password_request(self, testUser):
      data = {
         'email': testUser.email,
      }
      response = self.client.get(self.reset_password_request_url, data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.reset_password_expiration = dateparse.parse_datetime(response.json()['reset_password_expiration'])
   
   def reset_password(self, testUser):
      user = User.objects.get(email=testUser.email)
      data = {
         'email': testUser.email,
         'token': user.reset_password_token,
         'password': testUser.password+'_reset',
      }
      response = self.client.post(self.reset_password_url, data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      testUser.password = data['password']
        
class ClassicAuthenticationTestCase(AuthenticationTestBase):
   
   def test_classic_authentication(self):
      testUser = TestUser()
      self.signup(testUser)
      self.verify_email(testUser)
      self.login( testUser)
      self.changePassword(testUser)
      self.logout(testUser)
      self.login(testUser)
      self.logout(testUser)
      self.reset_password_request(testUser)
      self.reset_password(testUser)
      self.login(testUser)
      self.logout(testUser)

from django.test import RequestFactory

class GoogleAuthTest(AuthenticationTestBase):

   def test_google_login_view_flow(self):
      testUser = TestUser(email='testuser@gmail.com')

      def mock_get_user_info(access_token):
         return {'email': testUser.email} if access_token==testUser.access_token else None

      with patch('Authentication.views.get_user_info_from_google_token', side_effect=mock_get_user_info):
         for _ in range(2):
            from Authentication.views import GoogleLoginView
            data = {'code': testUser.access_token}
            request = self.factory.get(self.google_login_url, data)
            response = GoogleLoginView().get(request)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(User.objects.count(), 1)
            self.assertEqual(User.objects.get().email, testUser.email)
            user = User.objects.get()
            testUser.token = user.token
            self.logout(testUser)
   
   def add_google_social_app(self):
      SocialApp.objects.create(provider='Google', name='google', client_id=GOOGLE_CREDENTIALS['test']['client_id'], secret=GOOGLE_CREDENTIALS['test']['secret'])
   
   def test_get_user_info_from_google_token(self):
      testUser = TestUser(email='testuser@gmail.com')
      self.add_google_social_app()
      from Authentication.views import get_user_info_from_google_token
      response = get_user_info_from_google_token(testUser.access_token)
      self.assertDictEqual(response, {'error': 'invalid_request', 'error_description': 'Invalid Credentials'})