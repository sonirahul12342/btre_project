# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    '''USERNAME_FIELD = 'email'
    email = models.EmailField(('email address'), unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS'''
    phone=models.CharField(max_length=100)
    is_realtor=models.BooleanField(default=False)
    

    def __str__(self):
        return self.email
