from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

# Register your models here.

admin.site.register(Category,MPTTModelAdmin)
admin.site.register(Tracker)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress_Vendor)
admin.site.register(Product)
admin.site.register(cartItem)
admin.site.register(cart)
admin.site.register(Order)
admin.site.register(ShippingAddress_customer)