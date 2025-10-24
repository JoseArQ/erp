from django.db import models

class Company(models.Model):
    """
    Represents a company that can have multiple users.
    """
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
