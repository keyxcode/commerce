from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image_url = models.CharField(max_length=128, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    current_bid = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    num_bids = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="similar_listings")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="all_listings")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Bid(models.Model):
    pass


class Comment(models.Model):
    content = models.CharField(max_length=256)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)