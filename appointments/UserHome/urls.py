from django.contrib import admin
from django.urls import path,include
from . import views

# from Userhome.urls import link
urlpatterns=[
     path("",views.userhome,name='home'),
     path("bookingpage/",include("BookingPage.urls"),name="bookingpage"),
]