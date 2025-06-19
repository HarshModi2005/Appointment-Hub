from django.shortcuts import render,HttpResponse,redirect


# Create your views here.

# def bookingpage(request):
#     if request.method == "POST":
#         phonewa = request.POST.get('phonebook')
#         datewa = request.POST.get('datebook')
#         timewa = request.POST.get('timebook')
        
#         if phonewa:
            
#             bookingdetails = BookingDetails(phone=phonewa,date=datewa,time=timewa)
#             bookingdetails.save()
#             return HttpResponse("Booking Successful")
#     return render(request,'bookpage.html')