from django.shortcuts import render
from django.http import HttpRequest
from .models import *
from django.http import HttpResponse


from django.db.models import Max, Min
# Create your views here.

#SIgnup
def signup(request):
    postData = request.POST
    username = postData.get('username')
    firstname = postData.get('firstname')
    lastname = postData.get('lastname')
    phone = postData.get('phone')
    email = postData.get('email')
    password = postData.get('password')
    
    return render(request, 'signup.html')
#Login
def login(request):
    context = {}
    return render(request, 'login.html',context)

#Hotels home

def store(request):
    hotel = None
    locations = Location.get_all_locations()
    locationID = request.GET.get('location')
  
    
   
    
    
    if locationID:
        hotel = Hotel.get_all_location_by_locationid(locationID)
    else:
        hotel = Hotel.get_all_hotel();
        
    min_price = Hotel.objects.all().aggregate(Min('price'))
    max_price = Hotel.objects.all().aggregate(Max('price'))
    print(min_price)
    print(max_price)

    FilterPrice = request.GET.get('FilterPrice')
    
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        hotel = Hotel.objects.filter(price__lte = Int_FilterPrice)
    else:
        hotel = Hotel.objects.all()
		
		

    context = {}
    
    
    context  = {
        'hotel' :hotel,
        'locations' :locations,
        
        'min_price':min_price,
        'max_price':max_price,
		'FilterPrice':FilterPrice,
    }
    
    
   
    print('you are : ', request.session.get('email'))
    return render(request, 'store.html', context)



# Login as manager
def loginAsManager(request):
    context = {}
    return render(request, 'loginAsManager.html', context)
#manager deshbord
def managerdeshbord(request):
    context = {}
    return render(request, 'manager_deshbord.html', context)

def reservation (request):
    return render(request, "reservation.html")




# filter by price
   