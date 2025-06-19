from django.contrib import admin
from django.urls import path,include
from . import views




#Create your views here.


urlpatterns=[
    path("",views.userlogin,name='home'),
    path('<emailurl>/', views.userhome, name="userhomelink"),#userhome
    path('<nameurl>', views.bookingpage, name="bookingpagelink"),#bookingpage
    
   
]
