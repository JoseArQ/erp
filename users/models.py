from django.contrib.auth.models import AbstractUser
from django.db import models

from company.models import Company

from .enums import UserRole

class User(AbstractUser):
    role = models.CharField(
        max_length=20, 
        choices=UserRole.choices(), 
        default='employee',
        )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
        help_text="The company this user belongs to."
    )

    def __str__(self):
        return f"{self.username} ({self.role}) - {self.company}"