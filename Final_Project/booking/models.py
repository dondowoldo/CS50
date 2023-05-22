from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    
class PropertyType(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.type}"

    
class Listing(models.Model):
    title = models.CharField(max_length=100)
    price_per_night = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    date_created = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, null=True, related_name="property_type")
    active = models.BooleanField(default=True)
    imageurl = models.URLField(max_length=300, blank=True)
    location = models.CharField(max_length=20)
    geolat = models.FloatField(max_length=150)
    geolng = models.FloatField(max_length=150)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watching")
    description = models.TextField(max_length=300)
    availability_from = models.DateField()
    availability_to = models.DateField()
    available_dates = models.ManyToManyField('AvailableDate', blank=True, related_name="availability")

    def __str__(self):
        return f"{self.title} : {self.price_per_night} : {self.location}"
    

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
    startdate = models.DateField()
    enddate = models.DateField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.user} : {self.listing}, {self.timestamp}, {self.duration}, {self.total_price}"


class AvailableDate(models.Model):
    date = models.DateField()
    
    def __str__(self):
        return f"{self.date}"