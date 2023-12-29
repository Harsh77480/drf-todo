from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
import uuid

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    



class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
class EmailVerification(models.Model): 
    hash  = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    email = models.EmailField(unique = True,blank = False)