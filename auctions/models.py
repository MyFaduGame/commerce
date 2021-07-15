from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass

class Categories(models.Model):
    categories=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.categories}"

class Listings(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=64)
    description=models.CharField(max_length=400)
    start_bid=models.PositiveIntegerField()
    image=models.URLField(max_length=250, blank=True)
    category=models.ForeignKey(Categories, related_name="items", blank=True, null=True, on_delete=models.SET_NULL)
    last_modified=models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.id}: {self.title}"

class Watchlists(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    listings=models.ManyToManyField(Listings, related_name="watchlists")

    def __str__(self):
        return f"{self.id}: {self.listings} by {self.user}"

#def validate_bid(value):
#    if value <= value:
#        raise ValidationError("Sorry")
#    else:
#        return value

class Bid(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    current_bid=models.PositiveIntegerField(blank=False)
    listings=models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
    bid_time=models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.id}: {self.user} has bid {self.current_bid} for {self.listings}"

class Comments(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    listings=models.ForeignKey(Listings, on_delete=models.CASCADE)
    message=models.TextField()
    time_sent=models.DateTimeField()