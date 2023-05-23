from django.urls import path
from store.views import *

urlpatterns=[
   
    

    path('', homepage,name="homepage"),
    path('home', homepage,name="homepage"),
    path('about', aboutpage,name="aboutpage"),
    path('contact', contactpage,name="contactpage"),
    path('user', user_log_sign_page,name="userloginpage"),
    path('user/login', user_log_sign_page,name="userloginpage"),
    path('user/bookings', user_bookings,name="dashboard"),
    path('user/book-room', book_room_page,name="bookroompage"),
    path('user/book-room/book', book_room,name="bookroom"),
    path('user/signup', user_sign_up,name="usersignup"),
    path('staff/',staff_log_sign_page,name="staffloginpage"),
    path('staff/login', staff_log_sign_page,name="staffloginpage"),
    path('staff/signup', staff_sign_up,name="staffsignup"),
    path('logout', logoutuser,name="logout"),
    path('staff/panel', panel,name="staffpanel"),
    path('staff/allbookings', all_bookings,name="allbookigs"),
    
    path('staff/panel/add-new-location', add_new_location,name="addnewlocation"),
    path('staff/panel/edit-room', edit_room),
    path('staff/panel/add-new-room', add_new_room,name="addroom"),
    path('staff/panel/edit-room/edit', edit_room),
    path('staff/panel/view-room', view_room),
    
    path('feedback/<int:reservation_id>/', add_feedback, name='add_feedback'),
]

    
  
