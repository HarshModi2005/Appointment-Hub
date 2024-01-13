from django.shortcuts import render,HttpResponse,redirect
from .models import UserSignup

# Create your views here.


def usersignup(request):
    if request.method=="POST":
        fullname=request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        profession = request.POST.get('profession')
        address = request.POST.get('address')
        charges = request.POST.get('charges')
       
        if password and charges and phone:
            usersignup = UserSignup(fullname=fullname,email=email,password=password,phone=phone,city=city,state=state,profession=profession,address=address,charges=charges)
            usersignup.save()
            return redirect('/adminlogin')
        else:
            return redirect('/adminsignup')
    return render(request,'usignup.html')