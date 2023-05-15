from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    
class Listing(models.Model):
    name = models.CharField(max_length=100)
    price_per_day = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    date_created = models.DateTimeField(auto_now_add=True)
    property_type = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    imageurl = models.URLField(max_length=300, blank=True)
    location = models.CharField(max_length=30)
    gps_location = models.CharField(max_length=50)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watching")
    description = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"
    

class Comment(models.Model):
    comment = models.TextField(max_length=300, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user")
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="listing")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.comment}"
    

class Message(models.Model):
    sent_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.sent_from} : {self.sent_to} : {self.timestamp} : {self.message}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="property")
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.user} : {self.listing}, {self.timestamp}, {self.duration}, {self.total_price}"