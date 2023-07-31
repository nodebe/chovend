from django.db import models
from user.models import User
import uuid, json
from django.utils import timezone


class SocialMedia(models.Model):
    social_media = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(default=timezone.now)

class Country(models.Model):
    country_name = models.CharField(max_length=50, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.country_name

class State(models.Model):
    state_name = models.CharField(max_length=50, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.state_name

class City(models.Model):
    city_name = models.CharField(max_length=50, null=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.city_name
    
class Product(models.Model):
    id = models.CharField(max_length=36, primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=240)
    location = models.ForeignKey(City, on_delete=models.SET_NULL)
    social_media_urls = models.ManyToManyField(SocialMedia, through='ProductSocialMedia')
    website = models.URLField()
    images = models.CharField(max_length=1000, default='[]')
    date_created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4().hex)
        super().save(*args, **kwargs)
    
    def set_images(self, value):
        self.images = json.dumps(value)

    def get_images(self):
        return json.loads(self.images)

    def __str__(self):
        return self.user
