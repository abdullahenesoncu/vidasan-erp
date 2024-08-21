from allauth.account.signals import email_confirmed
from django.dispatch import receiver

@receiver(email_confirmed)
def handle_email_confirmed(sender, request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True
    user.save()