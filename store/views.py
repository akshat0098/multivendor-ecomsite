from django.views.decorators.csrf import csrf_exempt
from accounts.middleware import *
from accounts.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from .forms import *
from .models import *

# Create your views here.

def index(request):
    context = {}
    return render(request,'store/home_page.html',context)


#@allowed_users(allowed_roles=['vendor','admin'])
@login_required(login_url='login')
def Upload_Product(request):
    user = request.user
    try:
        vendor = Vendor.objects.get(user=user)
    except:
        return HttpResponse('To upload  Product you need to become a Vendor ')
    form = ProductCreationForm()
    if request.method == 'POST':
        form = ProductCreationForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data['title']
            unit_price = form.cleaned_data['unit_price']
            Category = form.cleaned_data['category']
            unit = form.cleaned_data['unit']
            dimension = form.cleaned_data['dimension']
            quantity = form.cleaned_data['quantity']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']
            aval = form.cleaned_data['Avaibility']
            #creating the product object 
            pro = Product.objects.create(vendor= vendor,title= title,unit_price= unit_price,
            category= Category ,unit = unit,dimension= dimension,
            quantity= quantity,location=location,description=description,Avaibility=aval)
            pro.save()
            form = ProductCreationForm()
            
        messages.success(request,' Product was Succesfully added' )
        
    context = {'form':form}
    return render(request,'store/product_upload.html',context)

@login_required(login_url='login')
def UpdateProduct(request,pk_test): 
    pass

def product_view(request):
    product = Product.objects.all()
    context = {'product':product}
    return render(request,'store/product.html',context)


#working on cart
@login_required(login_url='login')
def Cart(request,pk):
    user =   User.objects.get(id=request.user.id)
    #pk is the product id 
    prod =  Product.objects.get(id=pk)
    #get the cart
    try:
        CART = cart.objects.get(owner=user )
    except:
        CART = cart.objects.create(owner=user, cart_id=user.id)
        
    #crated cartitems
    item,created = cartItem.objects.get_or_create(user=request.user,cart= CART,
    product=prod,price=prod.unit_price )
  
    return HttpResponse('Congrat the item is added to cart')


@login_required(login_url='login')
def view_cart(request):
    CART,created  = cart.objects.get_or_create(owner=request.user,cart_id=request.user.id)
    #getting items
    print(CART)
    items= cartItem.objects.filter(cart=CART.id)
    if request.POST:
        qty = request.POST.get('qty')
        item_id =  request.POST.get('item')
        print(qty)
        print(item_id)
        #making changes in qty
        item = items.get(id=item_id)
        item.qty = qty
        item.save()

    items = cartItem.objects.filter(cart=CART)
    total_price = calc_total_price(items)
    print(total_price)
    CART.total_price = total_price
    CART.save()
    context = {'items':items,'cart':CART}
    return render(request,'store/view_cart.html',context)

def calc_total_price(items):
    amt = 0 
    try:
        for x in items:
            price = x.product.unit_price * x.qty
            amt += price
    except:
        amt += items.product.unit_price * items.qty

    return amt

    #processig order

@login_required(login_url='login')
def PlaceOrder(request,pk):    
    product_id = Product.objects.get(id=pk)
    form = PlaceOrderForm()
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            mode = form.cleaned_data['order_payment_mode']
            address = form.cleaned_data['shipping_address']
            
            order_save =Order.objects.create( product = product_id, quantity = quantity,order_payment_mode = mode,status = 'Order Recieved', shipping_address = address, )
            Tracker.objects.create(tracker_id = order_save.id, description = order_save.status, order = order_save,
            )
            
    context = {'form':form }
    return render(request,'store/place_order.html',context)



@login_required(login_url='login')
def order_tracker(request,pk):
    #tracker_details = Tracker.objects.get(tracker_id=pk)
    qs = Tracker.objects.filter(tracker_id=pk)
    #qs = qs.values()
    context = {'qs':qs}
    return render(request,'store/tracker.html',context)


@login_required(login_url='login')
def order_page(request):
    order = Order.objects.all()
    context = {'orders':order}
    return render(request,'store/order_view.html',context)



@login_required(login_url='login')
def Shipping(request):
    form = ShipCustomerForm()
    address = None
    if request.method == 'POST':
        form = ShipCustomerForm(request.POST,instance=request.user)
        if form.is_valid():
            address =form.save() 
            messages.success(request,'Address was succesfully added')
            
    context = {'form':form,'address': address}
    return  context
    #return render(request,'store/shipping.html',context)


def checkout(request):
    user = User.objects.get(id=request.user.id)
    form = ShipCustomerForm()
    orderform = OrderForm()
    address = None
    if request.method == 'POST':
        form = ShipCustomerForm(request.POST)
        orderform = OrderForm(request.POST)
        if form.is_valid():
            address= ShippingAddress_customer.objects.create(customer=request.user,Name=form.cleaned_data['Name'],
            Email=form.cleaned_data['Email'],
            phone_no=form.cleaned_data['phone_no'],
            address_line_1=form.cleaned_data['address_line_1'],
            address_line_2 =form.cleaned_data['address_line_2'],
            City =form.cleaned_data['City'],
            state = form.cleaned_data['state'] , 
            pincode = form.cleaned_data['pincode'] )
            
            messages.info(request,'address was succesfully added')
            #OrderForm passe
        address_id = address.id
        if orderform.is_valid():
            CART = cart.objects.get(owner=request.user.id)
            payment_mode = request.POST.get('order_payment_mode')
            print(payment_mode)
            try:
                items = cartItem.objects.filter(cart=CART)
                order_list = []
                #creating order 
                for item in items:
                    #crating the order item
                    order_price = item.product.unit_price * item.qty
                    order_item = OrderItem.objects.create(customer=request.user,
                    product=item.product,qty=item.qty,order_price=order_price)  
                    order_list.append(order_item) 
            #plceing the order
                print(type(request.POST.get('order_payment_mode')))
                if payment_mode == '2':
                    
                    return redirect('checkout-payment')
                else:
                    for order  in order_list:
                        Order.objects.create(customer=request.user,product_item = order,
                            order_payment_mode= payment_mode , shipping_address = address,status='Order Recieved'
                        )
            except:
                 return HttpResponse('There was no product at the cart')
       
    context = {'form':form,'orderform':orderform}
    return render(request,'store/checkout.html',context)


# Adding Payment Gateway
import razorpay

razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))
@login_required(login_url='login')
@csrf_exempt
def checkout_payment(request):
    CART = cart.objects.get(owner=request.user.id)
    context = {}
    order_temp =None
    items = cartItem.objects.filter(cart=CART)
    address = ShippingAddress_customer.objects.filter(customer=request.user).first()
    if(len(items)>0):
        order_list = []
        #creating order 
        for item in items:
            #crating the order item
            order_price = item.product.unit_price * item.qty
            order_item = OrderItem.objects.create(customer=request.user,
            product=item.product,qty=item.qty,order_price=order_price)  
            order_list.append(order_item)
            #creating order

        order_currency = 'INR'

        callback_url = "http://127.0.0.1:8000/checkout/payment/success"
        notes = {'order-type': "basic order from the website", 'key':'value'}
        
        for order  in order_list:
            order_temp = Order(customer=request.user,product_item = order,
            order_payment_mode= 2 , shipping_address = address,status='Order Recieved')
        
        razorpay_order = razorpay_client.order.create(
        dict(amount =CART.total_price,
        currency=order_currency, notes = notes,
        receipt=order_temp.order_id, payment_capture='0'))

        print(razorpay_order['id'])
        order_temp.razorpay_order_id = razorpay_order['id']
        order_temp.save()
        
        context = {'cart': CART, 'order_id':
        razorpay_order['id'],
        'orderId':order_temp.order_id, 
        'final_price':cart.total_price, 
        'razorpay_merchant_id':settings.razorpay_id,
        'callback_url':callback_url}

    else:

        return HttpResponse("No product in cart")
    
    return render(request,'payment/payment.html',context)

@csrf_exempt
def checkout_payment_success(request):
    return HttpResponse('Congratulation Your order is placed')