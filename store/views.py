from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from .models import Hotels,Rooms,Reservation,Feedback
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Max, Min
from .forms import FeedbackForm
from django.utils import timezone
# Create your views here.

#homepage
def homepage(request):
    all_location = Hotels.objects.values_list('location','id').distinct().order_by()
    if request.method =="POST":
        try:
            print(request.POST)
            hotel = Hotels.objects.all().get(id=int(request.POST['search_location']))
            rr = []
            
            #for finding the reserved rooms on this time period for excluding from the query set
            for each_reservation in Reservation.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.room.id)
                
            room = Rooms.objects.all().filter(hotel=hotel,capacity__gte = int(request.POST['capacity'])).exclude(id__in=rr)
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

#ALll rooms
def rooms(request):
    room = None
    available_rooms = len(Rooms.objects.all().filter(status='1'))
    print("the available rooms are:",available_rooms)
    min_price = Rooms.objects.all().aggregate(Min('price'))
    max_price = Rooms.objects.all().aggregate(Max('price'))
    print(min_price)
    print(max_price)

    FilterPrice = request.GET.get('FilterPrice')
    print("The filter price:",FilterPrice)
    # #img = Rooms.objects.filter(img = 'img')
    # img = request.GET.get('img')
    # print("img url",img)
    if available_rooms:
        if FilterPrice:
        
            Int_FilterPrice = int(FilterPrice)
            room = Rooms.objects.filter(price__lte = Int_FilterPrice)
        
    #     print("The rooms are:", room)
        else:
            room = Rooms.objects.all()
        
    print("the rooms are:",room)	
    # rooms = Rooms.objects.all()
    return render(request, 'user/room_list.html', {'room': room,'min_price': min_price, 'max_price': max_price,'FilterPrice':FilterPrice,})

#about
def aboutpage(request):
    return HttpResponse(render(request,'about.html'))

#contact page
def contactpage(request):
    return HttpResponse(render(request,'contact.html'))

#user sign up
def user_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request,"Password didn't matched")
            return redirect('userloginpage')
        
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Not Available")
                return redirect('userloginpage')
        except:
            pass
            

        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=False
        new_user.save()
        messages.success(request,"Registration Successfull")
        return redirect("userloginpage")
    return HttpResponse('Access Denied')
#staff sign up
def staff_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        

        if password1 != password2:
            messages.success(request,"Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass
        
        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=True
        new_user.save()
        messages.success(request," Staff Registration Successfull")
        return redirect("staffloginpage")
    else:

        return HttpResponse('Access Denied')
#user login and signup page
def user_log_sign_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pswd']

        user = authenticate(username=email,password=password)
        try:
            if user.is_staff:
                
                messages.error(request,"Incorrect username or Password")
                return redirect('staffloginpage')
        except:
            pass
        
        if user is not None:
            login(request,user)
            messages.success(request,"successful logged in")
            print("Login successfull")
            return redirect('homepage')
        else:
            messages.warning(request,"Incorrect username or password")
            return redirect('userloginpage')

    response = render(request,'user/userlogsign.html')
    return HttpResponse(response)

#logout for admin and user 
def logoutuser(request):
    if request.method =='GET':
        logout(request)
        messages.success(request,"Logged out successfully")
        print("Logged out successfully")
        return redirect('homepage')
    else:
        print("logout unsuccessfull")
        return redirect('userloginpage')

#staff login and signup page
def staff_log_sign_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        
        if user.is_staff:
            login(request,user)
            return redirect('staffpanel')
        
        else:
            messages.success(request,"Incorrect username or password")
            return redirect('staffloginpage')
    response = render(request,'staff/stafflogsign.html')
    return HttpResponse(response)

#staff panel page
@login_required(login_url='/staff')
def panel(request):

   
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    staff_id = request.user.id
    print("The staff number is:",staff_id)

    hotel = Hotels.objects.filter(staff_id = staff_id)
    
    
    print("the hotel name is :",hotel)
    rooms = Rooms.objects.filter(hotel__in=hotel)
    
    #rooms = Rooms.objects.filter(hotel_id = hotel )
    print("positive:",rooms)
    # else:
    #     rooms = Hotels.get_all_hotel()
    #     print("neg:",rooms)
    #rooms = Rooms.objects.all().filter(hotel=hotel)
    print(rooms)
    total_rooms = len(rooms)
    print("the total room fr 1 hotel:",total_rooms)
    available_rooms = len(Rooms.objects.all().filter(status='1'))
    print("The actual availibility before reservation:",available_rooms)
    unavailable_rooms = len(Rooms.objects.all().filter(status='2'))
    reserved = len(Reservation.objects.filter(room__hotel__in=hotel))
    #reserved = len(Reservation.objects.all())
    if reserved:
        # Process reservation form submission
        
        

            # Update available_rooms count
            available_rooms -= 1
    print("The available rooms are:",available_rooms)


    #hotel = Hotels.objects.filter(staff__id=staff_id).values_list('location', 'id').distinct().order_by()



    hotel = Hotels.objects.values_list('location','id').distinct().order_by()

    response = render(request,'staff/panel.html',{'location':hotel,'reserved':reserved,'rooms':rooms,'total_rooms':total_rooms,'available':available_rooms,'unavailable':unavailable_rooms})
    return HttpResponse(response)

#for editing room information
@login_required(login_url='/staff')
def edit_room(request):
    if request.user.is_staff == False:   
        return HttpResponse('Access Denied')
    if request.method == 'POST' and request.user.is_staff:
        print(request.POST)
        old_room = Rooms.objects.all().get(id= int(request.POST['roomid']))
        hotel = Hotels.objects.all().get(id=int(request.POST['hotel']))
        old_room.room_type  = request.POST['roomtype']
        old_room.capacity   =int(request.POST['capacity'])
        old_room.price      = int(request.POST['price'])
        old_room.size       = int(request.POST['size'])
        old_room.hotel      = hotel
        old_room.status     = request.POST['status']
        old_room.room_number=int(request.POST['roomnumber'])

        old_room.save()
        messages.success(request,"Room Details Updated Successfully")
        return redirect('staffpanel')
    else:
    
        room_id = request.GET['roomid']
        room = Rooms.objects.all().get(id=room_id)
        response = render(request,'staff/editroom.html',{'room':room})
        return HttpResponse(response)

#for adding room
from django.core.exceptions import ObjectDoesNotExist
@login_required(login_url='/staff')
def add_new_room(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        staff_id = request.user.id
        hotel_id = request.POST.get('hotel', None)
        try:
            hotel = Hotels.objects.get(id=hotel_id, staff_id=staff_id)
        except ObjectDoesNotExist:
            return HttpResponse('Hotel does not exist')
        
        room_type = request.POST['roomtype']
        capacity = int(request.POST['capacity'])
        size = int(request.POST['size'])
        status = request.POST['status']
        #img = request.POST['img']
        img = request.FILES.get('img')
        price = request.POST['price']

        print("###########", img)
        
       
        max_room_number = Rooms.objects.filter(hotel=hotel).aggregate(Max('roomnumber'))['roomnumber__max']
        room_number = max_room_number + 1 if max_room_number else 1

        new_room = Rooms(roomnumber=room_number, room_type=room_type, capacity=capacity, size=size,
                         hotel=hotel, status=status, img=img, price=price)
        new_room.save()

        messages.success(request, "New Room Added Successfully")

    return redirect('staffpanel')


# def add_new_room(request):
    

#     if request.user.is_staff == False:
#         return HttpResponse('Access Denied')
#     if request.method == "POST":
#         total_rooms = len(Rooms.objects.all())
#         new_room = Rooms()
#         staff_id = request.user.id
        

#         hotel = Hotels.objects.filter(staff_id=staff_id).values_list('location', 'id').distinct().order_by()
#         print(hotel)

#         hotel_id = request.POST.get('hotel', None)
#         try:
#             hotel = Hotels.objects.get(id=hotel_id)
#         except ObjectDoesNotExist:
#             # handle the exception here, e.g. return an error response
#             return HttpResponse('Hotel does not exist')
        
#         print(f"id={hotel.id}")
#         print(f"name={hotel.name}")

        
#         new_room = Rooms()
#         new_room.room_type  = request.POST['roomtype']
#         new_room.capacity   = int(request.POST['capacity'])
#         new_room.size       = int(request.POST['size'])
#         new_room.capacity   = int(request.POST['capacity'])
#         new_room.hotel      = hotel
#         new_room.status     = request.POST['status']
#         new_room.img = request.POST['img']
#         new_room.price      = request.POST['price']

#         new_room.save()
#         messages.success(request,"New Room Added Successfully")
    
#     return redirect('staffpanel')

#booking room page
@login_required(login_url='/user')
def book_room_page(request):
    room = Rooms.objects.all().get(id=int(request.GET['roomid']))
    return HttpResponse(render(request,'user/bookroom.html',{'room':room}))

#For booking the room
@login_required(login_url='/user')
def book_room(request):
    
    if request.method =="POST":

        room_id = request.POST['room_id']
        
        room = Rooms.objects.all().get(id=room_id)
        #for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(room = room):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("homepage")
            
        current_user = request.user
        total_person = int( request.POST['person'])
        booking_id = str(room_id) + str(datetime.datetime.now())

        reservation = Reservation()
        room_object = Rooms.objects.all().get(id=room_id)
        room_object.status = '2'
        
        user_object = User.objects.all().get(username=current_user)

        reservation.guest = user_object
        reservation.room = room_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request,"Congratulations! Booking Successfull")

        return redirect("homepage")
    else:
        return HttpResponse('Access Denied')


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    current_date = timezone.now().date()
    
    if request.method == 'POST':
        if reservation.check_out <= current_date:
            messages.success(request,'Cannot cancel a reservation that has already been checked out.')
        else:
       
            reservation.delete()
            messages.success(request, 'Reservation canceled successfully.')
        return redirect('room_list')  # Redirect to reservation list page or desired destination
    
    return render(request, 'user/cancel_reservation.html', {'reservation': reservation,'current_date':current_date})


def handler404(request):
    return render(request, '404.html', status=404)

@login_required(login_url='/staff')   
def view_room(request):
    room_id = request.GET['roomid']
    room = Rooms.objects.all().get(id=room_id)

    reservation = Reservation.objects.all().filter(room=room)
    return HttpResponse(render(request,'staff/viewroom.html',{'room':room,'reservations':reservation}))

@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(guest=user)
    # if not bookings:
    #     messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'user/mybookings.html',{'bookings':bookings}))

@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        owner = request.POST['new_owner']
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']
        
        hotels = Hotels.objects.all().filter(location = location , state = state)
        if hotels:
            messages.warning(request,"Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_hotel = Hotels()
            new_hotel.owner = owner
            new_hotel.location = location
            new_hotel.state = state
            new_hotel.country = country
            new_hotel.save()
            messages.success(request,"New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")
    

def store(request):
    room = None
    
    locations = locations.get_all_locations()
    locationID = request.GET.get('location')   
    
    if locationID:
        room = Hotels.get_all_location_by_locationid(locationID)
    else:
        room = Hotels.get_all_hotel()
        
    min_price = Rooms.objects.all().aggregate(Min('price'))
    max_price = Rooms.objects.all().aggregate(Max('price'))
    print(min_price)
    print(max_price)

    FilterPrice = request.GET.get('FilterPrice')
    
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        room = Rooms.objects.filter(price__lte = Int_FilterPrice)
    else:
        room = Rooms.objects.all()
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





    
#for showing all bookings to staff
@login_required(login_url='/staff')
def all_bookings(request):
    staff_id = request.user.id
    hotel = Hotels.objects.filter(staff_id = staff_id)

   
    #bookings = Reservation.objects.all()
    bookings = Reservation.objects.filter(room__hotel__in=hotel)
    # if not bookings:
    #     messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'staff/allbookings.html',{'bookings':bookings}))

@login_required(login_url='/user')
def add_feedback(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.reservation = reservation
            feedback.user = request.user
            feedback.save()
            #messages.success(request,"Thank you for your FeedBAck")
            return redirect('view_feedback',reservation_id=reservation_id)
 

    else:
        form = FeedbackForm()

    return render(request, 'user/add_feedback.html', {'form': form, 'reservation': reservation})


@login_required(login_url='/user')
def view_feedback(request,reservation_id):

    reservation = get_object_or_404(Reservation, id=reservation_id)
    room = reservation.room
    hotel = room.hotel
    feedback_entries = Feedback.objects.filter(reservation=reservation)
    return render(request, 'user/feedback_list.html', {'hotel': hotel, 'feedback_entries': feedback_entries})

@login_required(login_url='/user')
def delete_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        reservation_id = feedback.reservation_id
        feedback.delete()
        return redirect('view_feedback', reservation_id=reservation_id)
    except Feedback.DoesNotExist:
        return HttpResponse('Feedback does not exist')


        
@login_required(login_url='/user')
def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    reservation_id = feedback.reservation_id

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            
            return redirect('view_feedback',reservation_id = reservation_id)
    else:
        form = FeedbackForm(instance=feedback)

    return render(request, 'user/edit_feedback.html', {'form': form, 'feedback': feedback})






    


        