from django.urls import path
from store.views import *

urlpatterns=[
   
    path('',store,name = 'store'),
    
    path('reservation/',reservation ,name = 'reservation'),
    path('signup/',signup,name = 'signup'),
    path('login/',login,name = 'login'),
    path('loginManager/',loginAsManager,name ='manager'),
    path('manager_deshbord/',managerdeshbord,name = 'deshbord'),
    
    
]
    
