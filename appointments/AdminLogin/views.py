from django.shortcuts import render,HttpResponse,redirect

from UserSignup.models import UserSignup
from AdminSignup.models import AdminSignup
from UserLogin.models import BookingDetails
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

# Create your views here.
def adminlogin(request):
    if request.method == "POST":
        email = request.POST.get('emaillogin')
        password = request.POST.get('passwordlogin')
        
        emaillLogin = UserSignup.objects.filter(email = email).values('email','password')
        # if password == emaillLogin[0]['password']:
        #     return redirect('/adminhome')
        


        encrypted= mail_to_url(email)
        if emaillLogin and password == emaillLogin[0]['password']:
            
             
            return redirect('adminhomelink',emailurl=encrypted)




    return render(request,'alogin.html')

def adminhome(request,emailurl):
    # return HttpResponse("Admin Home Page")
    count=0
    city= None
    raasta = request.path
    raasta = raasta[0:len(raasta)-1]
    raasta= raasta[::-1]
    ind = raasta.index('/')
    raasta = raasta[0:ind]
    raasta= raasta[::-1]
    
    raasta2=""
    raasta2.lower()
    for i in raasta:
        
        raasta2+=i.lower()
    raasta2 = vigenere_decrypt(raasta2,"harsh")
    raasta2 += "@gmail.com"

    nombre = (UserSignup.objects.filter(email=raasta2).values('fullname'))
    # return HttpResponse(raasta2)
    QuerySet = BookingDetails.objects.filter(name= " " + nombre[0]['fullname']).values('phone','date','time')
    
    context={
        'QuerySet':QuerySet,
        
    }
    
    
    # return HttpResponse(city)
   
    
    
    return render(request,'ahome.html',context)

    