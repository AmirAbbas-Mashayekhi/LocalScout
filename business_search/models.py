from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)


class BookmarkedBusiness(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yelp_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    yelp_url = models.URLField()
    review_count = models.IntegerField()
    rating = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
