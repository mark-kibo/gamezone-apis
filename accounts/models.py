from django.db import models
import uuid
# Create your models here.
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    COUNTRY_CHOICES = [
        ('KE', 'Kenya'),
        ('TZ', 'Tanzania'),
        ('UGD', 'Uganda'),
    ]
    
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    location = models.TextField(max_length=255)
    profile_pic = models.ImageField(upload_to="media")

    def __str__(self):
        return str(self.id)


class GameZoneUser(AbstractUser):
    
    # Add any additional fields you need
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True )
