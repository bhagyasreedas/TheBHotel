from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from .models import *
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import AvailabilityForm
from django.http import HttpResponse
from store.reservations_functions import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from store.reservations_functions.availability import check_availability
from django.contrib.auth.models import User
from django.db.models import Max, Min
import datetime
# Create your views here.




#user login 
# def user_login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['pswd']

#         user = authenticate(username=email,password=password)
#         try:
#             if user.is_staff:
                
#                 messages.error(request,"Incorrect username or Password")
#                 return redirect('managerlogin')
#         except:
#             pass
        
#         if user is not None:
#             login(request,user)
#             messages.success(request,"successful logged in")
#             print("Login successfull")
#             return redirect('store')
#         else:
#             messages.warning(request,"Incorrect username or password")
#             return redirect('login')

#     response = render(request,'login.html')
#     return HttpResponse(response)





class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('store')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('store')
def checkout(request):
    return render(request, 'checkout.html')


#user signup
class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        firstname = postData.get('firstname')
        lastname = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'firstname': firstname,
            'lastname': lastname,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(firstname=firstname,
                            lastname=lastname,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(firstname, lastname, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('signup')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.firstname):
            error_message = "First Name Required !!"
        elif len(customer.firstname) < 3:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.lastname:
            error_message = 'Last Name Required'
        elif len(customer.lastname) < 3:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 digit Long'
        # elif customer.phone != '1'or'2'or'3'or'4'or'5'or'6'or'7'or'8'or'9'or'0':
        #     error_message= 'Phone number must be digit'
        
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message





#Hotels home


def home(request):
    all_location = Hotel.objects.values_list('location','id').distinct().order_by()
    if request.method =="POST":
        try:
            print(request.POST)
            hotel = Hotel.objects.all().get(id=int(request.POST['search_location']))
            rr = []
            
            #for finding the reserved rooms on this time period for excluding from the query set
            for each_reservation in Reservation.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.room.id)
                
            room = Room.objects.all().filter(hotel=hotel,capacity__gte = int(request.POST['capacity'])).exclude(id__in=rr)
            if len(room) == 0:
                messages.warning(request,"Sorry No Rooms Are Available on this time period")
            data = {'rooms':room,'all_location':all_location,'flag':True}
            response = render(request,'index.html',data)
        except Exception as e:
            messages.error(request,e)
            response = render(request,'index.html',{'all_location':all_location})


    else:
        
        
        data = {'all_location':all_location}
        response = render(request,'index.html',data)
    return HttpResponse(response)

    

def store(request):
    room = None
    locations = Location.get_all_locations()
    locationID = request.GET.get('location')   
    
    if locationID:
        room = Hotel.get_all_location_by_locationid(locationID)
    else:
        room = Hotel.get_all_hotel()
        
    min_price = Room.objects.all().aggregate(Min('price'))
    max_price = Room.objects.all().aggregate(Max('price'))
    print(min_price)
    print(max_price)

    FilterPrice = request.GET.get('FilterPrice')
    
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        room = Room.objects.filter(price__lte = Int_FilterPrice)
    else:
        room = Room.objects.all()
    print(room)
		
		

    context = {}
    
    
    context  = {
        'room' :room,
        'locations' :locations,
        
        'min_price':min_price,
        'max_price':max_price,
		'FilterPrice':FilterPrice,
    }
    
    
   
    print('you are : ', request.session.get('email'))
    return render(request, 'room.html', context)





def reservation (request):
    model = Reservation
    reservation_list = Reservation.objects.all()
    print(reservation_list)
    

    return render(request, "reservation.html")


from django.core.exceptions import ValidationError

# class ReservationView(FormView):
#     form_p = AvailabilityForm
#     template_name = "availability_form.html" 
    
#     def form_valid(self,forms):
#         data = forms.cleaned_data 
#         room_list = Room.objects.filter(category=data['room_category'])
#         available_room = []
#         for room in room_list:
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_room.append(room)
               
                
#         if len(available_room)>0:
            
        
#             room = available_room[0]
            
#             reservation = Reservation.objects.create(
#                 user = self.request.user,
#                 room = room,
#                 check_in = data['check_in'],
#                 check_out =data['check_out']
#                 )
#             reservation.save()
#             return HttpResponse(reservation)
#             #return super().form_valid(form)
#         else:
#             raise ValidationError("No available rooms.")
# def reservation_success(request):
#     return HttpResponse('Reservation successful!')       
                
 #booking room page
#@login_required(login_url='signup')
def book_room_page(request):
    room = Room.objects.all().get(id=int(request.GET['roomid']))
    return HttpResponse(render(request,'bookroom.html',{'room':room}))

#For booking the room
@login_required(login_url='signup')
def book_room(request):
    
    if request.method =="POST":

        room_id = request.POST['room_id']
        
        room = Room.objects.all().get(id=room_id)
        #for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(room = room):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("store")
            
        current_user = request.user
        total_person = int( request.POST['person'])
        booking_id = str(room_id) + str(datetime.datetime.now())

        reservation = Reservation()
        room_object = Room.objects.all().get(id=room_id)
        room_object.status = '2'
        
        user_object = Customer.objects.all().get(firstname=current_user).first()

        reservation.user = user_object
        reservation.room = room_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request,"Congratulations! Booking Successfull")

        return redirect("store")
    else:
        return HttpResponse('Access Denied')
               
            
        
                
                
        
    