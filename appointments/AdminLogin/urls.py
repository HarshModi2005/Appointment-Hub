from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path("",views.adminlogin,name='home'),
    path("<emailurl>/",views.adminhome,name="adminhomelink")
]