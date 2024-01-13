from django.shortcuts import render,HttpResponse,redirect
# Create your views here.
from .models import AdminSignup

def adminsignup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        print(email,password,phone,city,state)
        if password and phone:
            usersignup = AdminSignup(email=email,password=password,phone=phone,city=city,state=state)
            usersignup.save()
            return redirect('/userlogin')
        else:
            return redirect('/usersignup')

    return render(request,'asignup.html')

