from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(blank=True, max_length=40, unique=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    address = models.CharField(blank=True, max_length=100)
    cac_id = models.CharField(blank=True, max_length=100)
    

    def __str__(self):
        return self.email

# class PersonProfile(models.Model):
#     user = 