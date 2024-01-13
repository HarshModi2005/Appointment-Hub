from django.shortcuts import render,HttpResponse,redirect
from UserSignup.models import UserSignup

# Create your views here.
def userhome(request,emailurl):
   
    city= None
   
    if request.method == "POST":
        city= request.POST.get('city')
    QuerySet = UserSignup.objects.filter(city=city).values('fullname','profession','charges')
    context={
        'QuerySet':QuerySet,
        'emailurl':emailurl
    }
        
    # return HttpResponse(city)
    
    return render(request,'professional_base.html',context)


# def new(request,emailurl):
    
#     context={'emailurl':emailurl}
#     return render(request,'uhome.html',context)
    