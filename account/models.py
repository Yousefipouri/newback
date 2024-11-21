
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


# Create your models here.

class MyUser(AbstractUser):
    phone_number = models.CharField(max_length=15)

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Ensure correct timezone comparison
        current_time = timezone.now()  # Use Django's timezone-aware current time
        time_elapsed = current_time - self.created_at
        return time_elapsed < timedelta(minutes=5)    