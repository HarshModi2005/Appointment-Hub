from django.db import models

# Create your models here.
class UserSignup(models.Model):
        fullname=models.CharField(max_length=50)
        password = models.CharField(max_length=50)
        email = models.EmailField(max_length=50)
        phone = models.IntegerField()
        city = models.CharField(max_length=50)
        state = models.CharField(max_length=50)
        profession = models.CharField(max_length=50)
        address= models.CharField(max_length=50)
        charges= models.IntegerField()
        
        

        
    
        def __str__(self):
            return self.email