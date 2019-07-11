from django.db import models
from datetime import datetime
from users.models import CustomUser
# Create your models here.
class Realtor(models.Model):
    name=models.CharField(max_length=40)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    photo=models.ImageField(upload_to='media/')
    description=models.TextField()
    phone=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    
    is_mvp=models.BooleanField(default=False)
    hire_date=models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.name