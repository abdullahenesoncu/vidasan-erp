from django.db import models

from django.contrib.auth.models import AbstractUser
from backend.models import BaseModel, Enum

class UserType( Enum ):
   ADMIN = 'Admin'
   PLANLAMA = 'Planlama'
   SATIS_PAZARLAMA = 'Satış/Pazarlama'
   KALITE_KONTROL = 'Kalite kontrol'
   DEPO = 'Depo'

class User(AbstractUser, BaseModel):
   name = models.CharField(max_length=300)
   email_verified = models.BooleanField(default=False)
   user_verified = models.BooleanField(default=False)
   user_type = models.CharField(max_length=100, choices=UserType.get_choices(), default=UserType.DEPO)
   token = models.CharField(max_length=300, null=True, blank=True)
   reset_password_token = models.CharField(max_length=300, null=True, blank=True)
   reset_password_expiration = models.DateTimeField(null=True, blank=True)

   def __str__(self):
      return self.name
