from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse,path
from AdminSignup.models import AdminSignup
from UserSignup.models import UserSignup
from .models import BookingDetails
from datetime import datetime
import string



def vigenere_matrix():
    #generates a vigenere matrix
    l=list(string.ascii_lowercase)
    rulebox=[]#empty list
    rulebox.append(l)
    for i in range(len(l)):
        rulebox.append(l)#appends the list
        j=list(l.pop(0))#removes the last element and stores it
        l=l+j#adds in a way such that it gets displaces by 1 unit
    return rulebox



def vigenere_encrypt(s,password):
    '''Encrypt the string s based on the password the vigenere cipher way and
    return the resulting string'''
    l=string.ascii_lowercase
    rulebox=vigenere_matrix()
    encrypted=""#encrypted data
    password_extend=""#empty string for extending the password
    cursor=0#tracks the position
    for i in range(len(s)):
        password_extend+=password[cursor]
        cursor+=1
        if cursor>len(password)-1:#if the password is exhausted it starts repeating
            cursor=0
    #it is similar to a matrix. we need to find 2 parameters : row and column. one we get by password and the other by plain text
    
    for i in range(len(s)):
        if s[i] in l:
            j=l.index(s[i])#finds the column
        else:
            continue
        k=l.index(password_extend[i])#finds the row
        
        encrypted+=rulebox[k][j]#adds the specific element
    return encrypted

def vigenere_decrypt(s,password):
    '''Decrypt the string s based on the password the vigenere cipher way and
    return the resulting string'''
    l=string.ascii_lowercase
    rulebox=vigenere_matrix()#viegenere matrix
    password_extend=""
    decrypted=""#decrypted string
   
    cursor=0
    for i in range(len(s)):#password extender
        password_extend+=password[cursor]
        cursor+=1
        if cursor>len(password)-1:
            cursor=0
    position=0
    for i in range(len(s)):
        position=rulebox[l.index(password_extend[i])]#fetches the row
        row=position.index(s[i])#goes into the row and fetches the column number
        decrypted+=l[row]#adds the corresponding letter
    return decrypted   
def mail_to_url(email):
    email2=""
    
    for i in email:
        if i == '@' :
            break
        elif i.isnumeric():
            continue
        else:
            email2+=i.lower()
    encrypted = vigenere_encrypt(email2,"harsh")
    return encrypted

def url_to_name(raasta):
    raasta= raasta[::-1]
    ind = raasta.index('/')
    raasta = raasta[0:ind]
    raasta= raasta[::-1]
    encrypted = vigenere_decrypt(raasta,"harsh")
    
    
    
    raasta2=""
    raasta2.lower()
    for i in encrypted:
        
        raasta2+=i.lower()
    raasta2 += "@gmail.com"
    return raasta2

def userlogin(request):
    
    
    if request.method == "POST":
        email = request.POST.get('emaillogin')
        password = request.POST.get('passwordlogin')
        
        emaillLogin = AdminSignup.objects.filter(email = email).values('email','password')
        encrypted= mail_to_url(email)
        
        if emaillLogin and password == emaillLogin[0]['password']:
            
             
            return redirect('userhomelink', emailurl=encrypted)
            
        
    
    return render(request,'ulogin.html')


# Create your views here.
def userhome(request,emailurl):
    count=0
    city= None
    raasta = request.path
    raasta2 = url_to_name(raasta)
    if request.method == "POST":
        city= request.POST.get('city')
    QuerySet = UserSignup.objects.filter(city=city).values('fullname','profession','charges')
    context={
        'QuerySet':QuerySet,
        'emailurl':emailurl,
        'raasta': raasta2,
    }
    
    if count>0:
        puranam = QuerySet[count-1]['fullname']
        return redirect('bookingpagelink',nameurl=raasta2)
    # return HttpResponse(city)
   
    
    
    return render(request,'professional_base.html',context)

    

def bookingpage(request,nameurl):
    raasta = request.path
    poora_naam=""
    for i in raasta:
        
        if i.isalpha():
            if i.isupper():
                 poora_naam+= " "
            poora_naam+=i
        
    poora_naam= poora_naam[9::]
    context ={ 'nameurl':nameurl,}
    
    if request.method == "POST":
        phonewa = request.POST.get('phonebook')
        datewa = request.POST.get('datebook')
        timewa = request.POST.get('timebook')
        fullnamewa = poora_naam
        
        
        if phonewa:
            
            bookingdetails = BookingDetails(phone=phonewa,date=datewa,time=timewa,name=fullnamewa)
            bookingdetails.save()
            return HttpResponse("Booking Successful")
        
    return render(request,'bookpage.html',context)

