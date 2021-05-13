from django.forms import ModelForm , formset_factory
from .models import *
from django import forms

class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['vendor']
        fields = '__all__'


class ShipCustomerForm(ModelForm):


    class Meta:
        model = ShippingAddress_customer
        fields = '__all__'
        exclude= ['customer','address_id']


class OrderForm(forms.Form,ModelForm):
    class Meta:

        model = Order

        fields = ['order_payment_mode']


class PlaceOrderForm(forms.Form,ModelForm):
    class Meta:

        model = Order

        fields = ['order_payment_mode'
        ]


