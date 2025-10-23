from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import UserRole

class User(AbstractUser):
    role = models.CharField(
        max_length=20, 
        choices=UserRole.choices(), 
        default='employee',
        )

    def __str__(self):
        return f"{self.username} ({self.role})"