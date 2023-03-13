from django.db import models

from django.conf import settings
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
    
# class Emenities(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    
    
    @staticmethod
    def get_all_locations():
        return Location.objects.all()

    def __str__(self):
        return self.name
    

    
class Hotel(models.Model):
    hotel_name = models.CharField(max_length= 100)
    
    hotel_description = models.TextField()
    
    
    # emenities = models.ManyToManyField(Emenities)
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
    
class Room(models.Model):
  
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    Room_Categories = ( 
                       ('WAC','AC'),
                       ('NAC','NON_AC'),
                       ('DEL','DELUXE'),
                       ('KIN','KING'),
                       ('QUE','QUEEN'))
    category = models.CharField(max_length=3, choices=Room_Categories)
    beds = models.IntegerField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    hotel_image = models.ImageField(upload_to ='uploads/')
    
    @staticmethod
    def get_rooms_by_id(ids):
        return Room.objects.filter(id__in =ids)

    @staticmethod
    def get_all_room():
        return Room.objects.all()
    
    def __str__(self):
        return f'{self.room_number},{self.category} with {self.beds} for {self.capacity} people'
    
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE,default = 1)
    check_in = models.DateTimeField(auto_now =False)
    check_out = models.DateTimeField(auto_now=False)
    
    
    
    #booking_id = models.CharField(max_length=100,default="null")

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in} to {self.check_out}'