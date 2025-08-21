from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('donor', 'Donor'),
        ('requester', 'Requester'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='requester')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Keep username required if you're using it

    def __str__(self):
        return f"{self.username} ({self.role})"
