
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Location)
admin.site.register(Reservation)
