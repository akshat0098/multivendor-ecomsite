from django.db import models
from django.contrib.auth.models import User

from ecom import settings

# Create your models here.

choices = (('Electrical','Electrical'),
    ('Carpenter','Carpenter'),
    ('Plumbing','Plumbing'),
   ('Hardware','Hardware'),)

class Vendor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    auth_token = models.CharField(max_length=100,null=True)
    is_verified = models.BooleanField(default=False,null=True)
    created_id = models.DateTimeField(auto_now_add=True,null=True)
    
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=300,null=True)
    phone_no = models.IntegerField(null=True)
    trade_name = models.CharField(max_length=100,null=True,blank=False)
    address = models.CharField(max_length=100,null=True,blank=False)
    NATURE_OF_SUPPLY = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Name
    
class Customer(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    customer_id =  models.IntegerField(null=True)
    Name = models.CharField(max_length=100,null=True)
    Phone_no = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return  self.user


