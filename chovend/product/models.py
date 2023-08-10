'This is the file that holds the models'

import uuid
import json
from django.db import models
from django.utils import timezone
from user.models import User


class SocialMedia(models.Model):
    "Model for the Different Social media channels"
    social_media = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.social_media)


class Country(models.Model):
    "Model to Store Country"
    country_name = models.CharField(max_length=50, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.country_name)


class State(models.Model):
    "Model to store states"
    state_name = models.CharField(max_length=50, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.state_name)


class City(models.Model):
    "Model to store cities"
    city_name = models.CharField(max_length=50, null=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.city_name)


class Product(models.Model):
    "Product model in postgreSQL"
    id = models.CharField(max_length=36, primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user')
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=1000, default='')
    search_description = models.CharField(max_length=1000, default='')
    location = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='location')
    social_media_urls = models.ManyToManyField(
        SocialMedia, through='ProductSocialMedia')
    website = models.URLField(null=True, blank=True)
    images = models.CharField(max_length=1000, default='[]')
    date_created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4().hex)

        # Save the search_description as a non-duplicate #Unordered but doesn't matter
        self.search_description = ' '.join(set(self.description.split()))

        super().save(*args, **kwargs)

    def set_images(self, value):
        "Set the image list to a json before saving"
        self.images = json.dumps(value)

    def get_images(self):
        "Get the image list of the product"
        return json.loads(self.images)

    def location_indexing(self) -> str:
        "Returns the flat string of a product's location"
        country = self.location.state.country.country_name
        state = self.location.state.state_name
        city = self.location.city_name

        return f"{city} {state}, {country}"

    def __str__(self) -> str:
        return str(self.title)


class ProductSocialMedia(models.Model):
    "Table linking Product and Social Media"
    social_media = models.ForeignKey(
        SocialMedia, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField(max_length=1000)
