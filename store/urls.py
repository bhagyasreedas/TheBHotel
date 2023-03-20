from django.urls import path
from store.views import *

urlpatterns=[
   
    path('',home,name = 'store'),
    path('room',store,name = 'room'),
    
    path('reservation/',reservation ,name = 'reservation'),
    path('signup',Signup.as_view(),name = 'signup'),
    path('login',Login.as_view(),name = 'login'),
    path('booking', ReservationView.as_view(),name = 'booking'),
    path('reservation/success/', reservation_success, name='reservation_success'),
#    path('staff/',staff_log_sign_page,name="staffloginpage"),
#     path('staff/login', staff_log_sign_page,name="staffloginpage"),
#     path('staff/signup', staff_sign_up,name="staffsignup"),
#     path('staff/panel', panel,name="staffpanel"),
#     path('staff/allbookings', all_bookings,name="allbookigs"),
    path('logout/',logout,name = 'logout'),
    path('checkout/',checkout,name = 'checkout'),
    
    
]
    
