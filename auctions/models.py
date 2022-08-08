from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.id}: {self.username}"


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image_url = models.CharField(max_length=128, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    current_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    num_bids = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="creator_listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Bid(models.Model):
    value = models.DecimalField(max_digits=7, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="current_bid")

    def __str__(self):
        return f"Bid: {self.value} for {self.listing} by {self.bidder}"


class Comment(models.Model):
    content = models.CharField(max_length=256)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment {self.id}: {self.commenter} on {self.listing}: {self.content}"


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watcher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watcher}: {self.listing}"