from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

def generated_username():
    return "user_" + str(uuid.uuid4())[:5]

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    
    def __str__(self):
        return f"{self.username}'s account"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userid = models.CharField(max_length=50, unique=True, default=generated_username)
    
    
    def __str__(self):
        return f"{self.username}'s profile"
    
class Agency(models.Model):
    agency_logo = models.ImageField(upload_to='agencies_logos', default='1384014.png')
    agency_name = models.CharField(max_length=50, unique=True, null=False)
    total_bus = models.IntegerField(default=5, null=False, blank=False)
    agency_description = models.TextField()
    ceo_name = models.CharField(max_length=50, null=False)
    manager_name = models.CharField(max_length=50, null=True)
    date_created = models.DateField()
    location = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.agency_name} located in {self.location}"
    
def generate_bus_id():
    return "BUS_" + str(uuid.uuid4())[:3]
    
class Bus(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="buses")
    bus_number = models.CharField(max_length=50, unique=True, default=generate_bus_id)
    total_seats = models.IntegerField()
    
    def __str__(self):
        return f"{self.agency.agency_name} - Bus No: {self.bus_number}"
    
class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=1)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.origin} -> {self.destination} using Bus {self.bus.bus_number} at {self.departure_time}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} -> {self.route}"