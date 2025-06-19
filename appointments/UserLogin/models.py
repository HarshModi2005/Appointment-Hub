from django.db import models

# Create your models here.
class BookingDetails(models.Model):
    name= models.CharField(max_length = 100)
    
    phone = models.IntegerField()
  
    date = models.DateField()
    time = models.TimeField()