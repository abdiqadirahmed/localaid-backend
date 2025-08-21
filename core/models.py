from django.db import models
from django.conf import settings

class AidRequest(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('shelter', 'Shelter'),
        ('water', 'Water'),
        ('healthcare', 'Healthcare'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aid_requests')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.category}"


class DonatedResource(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('food', 'Food'),
        ('clothes', 'Clothes'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ])
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)   
    longitude = models.FloatField(null=True, blank=True)
    is_claimed = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.donor.username}"