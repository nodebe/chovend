from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class User(models.Model):
    id = models.UUIDField(max_length=36, primary_key=True, null=False)
    email = models.EmailField(null=False, unique=True)
    fullname = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=120, null=False)
    ip_address = models.GenericIPAddressField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4().hex)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email



class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    otp_value = models.IntegerField(null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email