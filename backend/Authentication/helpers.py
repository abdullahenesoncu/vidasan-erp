import random
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from backend.settings import FRONTEND_URL, RESET_PASSWORD_REDIRECT_PATH, SITE_NAME
from rest_framework.permissions import BasePermission

def get_random_string(n=12):
   res = ''
   for i in range(n):
      res += chr(ord('a')+random.randint(0, 25))
   return res

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_password_reset_mail(self, request, user):
        context = {
            "username": user.name,
            "password_reset_url": FRONTEND_URL + RESET_PASSWORD_REDIRECT_PATH + f'?token={user.reset_password_token}',
            "site_name": SITE_NAME,
        }

        # Render the email template with the given context
        email_subject = "Password Reset"
        email_template = "account/email/password_reset_key_message.txt"
        email_body = render_to_string(email_template, context)

        # Send the email
        email_message = EmailMessage(email_subject, email_body, to=[user.email])
        email_message.content_subtype = "html"  # Set the content type as HTML
        email_message.send()

class IsUserVerified(BasePermission):
    """
    Allows access only to authenticated and verified users.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_verified