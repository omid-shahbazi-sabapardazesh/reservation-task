from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core_auth.managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class UserType(models.TextChoices):
        NORMAL = 'normal'
        OWNER = 'owner'

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.NORMAL
    )

    def is_owner(self) -> bool:
        return self.user_type == self.UserType.OWNER