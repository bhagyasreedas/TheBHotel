"""TheBHotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import store.views as views
urlpatterns = [
    path('', views.homepage,name="homepage"),
    path('rooms/', views.rooms, name='room_list'),
    path('home', views.homepage,name="homepage"),
    path('about', views.aboutpage,name="aboutpage"),
    path('contact', views.contactpage,name="contactpage"),
    path('user', views.user_log_sign_page,name="userloginpage"),
    path('user/login', views.user_log_sign_page,name="userloginpage"),
    path('user/bookings', views.user_bookings,name="dashboard"),
    path('user/book-room', views.book_room_page,name="bookroompage"),
    path('user/book-room/book', views.book_room,name="bookroom"),
    path('reservation/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('user/signup', views.user_sign_up,name="usersignup"),
    path('staff/', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/login', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/signup', views.staff_sign_up,name="staffsignup"),
    path('logout', views.logoutuser,name="logout"),
    path('staff/panel', views.panel,name="staffpanel"),
    path('staff/allbookings', views.all_bookings,name="allbookigs"),
   
    path('staff/panel/add-new-location', views.add_new_location,name="addnewlocation"),
    path('staff/panel/edit-room', views.edit_room),
    path('staff/panel/add-new-room', views.add_new_room,name="addroom"),
    path('staff/panel/edit-room/edit', views.edit_room),
    path('staff/panel/view-room', views.view_room),

    path('admin/', admin.site.urls),
    path('feedback/<int:reservation_id>/add/', views.add_feedback, name='add_feedback'),
    path('feedback/<int:reservation_id>/', views.view_feedback, name='view_feedback'),
    path('feedback/<int:feedback_id>/edit/', views.edit_feedback, name='edit_feedback'),
    path('feedback/<int:feedback_id>/delete/', views.delete_feedback, name='delete_feedback'),


    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

