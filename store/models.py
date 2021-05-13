from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from mptt.models import MPTTModel,TreeForeignKey
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.models import User
import uuid
#from ecom import settings
from accounts.models import *

# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=50,unique=True)
    parent = TreeForeignKey('self',null=True,blank=True,related_name='children',db_index =True,on_delete=models.CASCADE)
    slug = models.SlugField(null=True,blank=False,default='slug')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent','slug',))
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors= [i.slug for i in ancestors]

        slugs= []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs


import uuid
class Product(models.Model):
    UNIT = (
        ('Kg','Kg'),
        ('sq. meter','sq. meter'),
        ('piece','piece'),
        ('gm','gm'),
        ('ft','ft'),
        ('meter','meter'),
        ('inch','inch'),
        ('length * thickness* breadth','length * thickness* breadth'),
        ('length * breadth', 'length * breadth'),
    )

    vendor = models.ForeignKey(Vendor,null=True,blank=False,on_delete=models.SET_NULL) 
   
    title = models.CharField(max_length=200,null=True,blank=False)
    #unit price is price per unit --> all prices is in INR.
    unit_price = models.FloatField(null=True,blank=False)
    #CATEGORY --> Nature of supply

    category = TreeForeignKey('Category',
                              null=True,
                              on_delete=models.CASCADE
                            )
    unit = models.CharField(max_length=150,null=True,choices=UNIT)
    #slug = models.SlugField(null=True,blank=False,default='slug')
    dimension = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.FloatField(null=True,blank=False)
    location = models.CharField(max_length=150,blank=True)
    Avaibility = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=1000,null=True,blank=False)
    date_created = models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self):
        return self.title



class ShippingAddress_customer(models.Model):
    customer = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    Name = models.CharField(max_length=100, null=False, blank=False)
    Email = models.EmailField(null=False, blank=False)
    phone_no = models.CharField(max_length=10,null=True,blank=False,help_text='Example: 9489237834')
    address_line_1 = models.CharField(max_length=300, null=False, blank=False)
    address_line_2 = models.CharField(max_length=300, null=False, blank=True)
    City = models.CharField(max_length=25, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    pincode = models.CharField(max_length=6,null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    address_id = models.SlugField(null=True)

    def __str__(self):
        return self.Name


  


class cart(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    cart_id = models.IntegerField(null=True)
    total_price = models.FloatField(null=True)


    def __str__(self):
        return str(self.owner)


class cartItem(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(null=True)
    cart = models.ForeignKey(cart,on_delete=models.CASCADE,null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    qty = models.IntegerField(default=1)

   



    
class ShippingAddress_Vendor(models.Model):
    vendor = models.ForeignKey(Vendor,null=True,on_delete=models.SET_NULL)
    Name = models.CharField(max_length=100,null=True,blank=False)
    Email = models.EmailField(null=True, blank=False)
    phone_no = models.IntegerField(null=True,blank=False)
    address = models.CharField(max_length=10000,null=True,blank=False)
    Destrict = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True,blank=False)
    pincode = models.CharField(max_length=6,null=True,blank=False)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.vendor.user.username




class OrderItem(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    qty = models.IntegerField(null=True)
    product_price = models.IntegerField(null=True)
    order_price = models.IntegerField(null=True)

    def __str__(self):
        return str(self.product)
    
class Order(models.Model):
    STATUS= (
        ('Order Recieved','Order Recieved'),
        ('Order Accepted','Order Accepted'),
        ('Out for delivery ','Our for delivery '),
        ('Deliverd','Delivered'), )

    PAYMENT = (
        (1 ,'Cash On Delivery'),
        (2,'Pay now'))
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
        (4,'PAY ON DELIVERY')
    )

    customer =  models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    product_item = models.ForeignKey(OrderItem,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(null=True,auto_now_add=True)
    
    order_payment_mode = models.IntegerField(max_length=25,null=True,blank=False,choices=PAYMENT)
    
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    shipping_address = models.ForeignKey(ShippingAddress_customer,null=True,on_delete=models.SET_NULL)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)

    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(auto_now_add=True,null=True)


    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return str(self.product_item.product) 




class Tracker(models.Model):
    order = models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    #logister_dealer
    tracker_id = models.IntegerField(null=True)
    description = models.CharField(max_length=150,null=True,default='')
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    @property
    def return_desc(self):
        return self.description

    @property
    def return_time(self):
        return self.timestamp
