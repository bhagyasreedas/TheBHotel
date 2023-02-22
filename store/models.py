from django.db import models
from django.contrib.auth.models import User

from django.db.models import Avg
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Customer(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    password = models.CharField(max_length=255)
    
    
    def register(self):
        self.save()
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


def isExists(self):
    if Customer.objects.filter(email = self.email):
        return True

    return  False
    
class Emenities(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    
    
    @staticmethod
    def get_all_locations():
        return Location.objects.all()

    def __str__(self):
        return self.name
    
class Hotel(models.Model):
    hotel_name = models.CharField(max_length= 100)
    Availability = models.IntegerField(default='0')
    hotel_description = models.TextField()
    hotel_image = models.ImageField(upload_to ='uploads/')
    price = models.IntegerField()
    emenities = models.ManyToManyField(Emenities)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    
    @staticmethod
    def get_hotels_by_id(ids):
        return Hotel.objects.filter(id__in =ids)

    @staticmethod
    def get_all_hotel():
        return Hotel.objects.all()

    @staticmethod
    def get_all_hotel_by_hotelid(location_id):
        if location_id:
            return Hotel.objects.filter(location = location_id)
        else:
            return Hotel.get_all_hotel();    
    def __str__(self):
        return self.hotel_name
    

class Reservation(models.Model):
    Name = models.CharField(max_length=20)
    Phone = models.IntegerField(default=0)
    Email = models.EmailField(max_length=40)
    Date_Check_In = models.DateField(auto_now=False)
    Date_Check_Out  = models.DateField(auto_now=False)
    Adulte = models.IntegerField (default=0)
    Children = models.IntegerField(default=0)
    Note = models.TextField()
    def __str__(self):
        return self.Name