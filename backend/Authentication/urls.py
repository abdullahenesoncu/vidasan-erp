from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
   path('signup/', SignupView.as_view(), name='auth_signup'),
   path('login/', LoginView.as_view(), name='auth_login'),
   path('logout/', LogoutView.as_view(), name='auth_logout'),
   path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
   path('reset-password-request/', ResetPasswordRequestView.as_view(), name='auth_reset_password_request'),
   path('reset-password/', ResetPasswordView.as_view(), name='auth_reset_password'),
   path('google/login/', GoogleLoginView.as_view(), name='auth_google_login'),
   path('users/', UserListCreateView.as_view(), name='user-list-create'),
   path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]