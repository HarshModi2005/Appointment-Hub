from django.db import models

# Create your models here.
class AdminSignup(models.Model):
    """
    Represents an admin signup in the system.
    """

    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    

    def __str__(self):
        return self.email