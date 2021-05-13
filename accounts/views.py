from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import login as dj_login , authenticate , logout 
from django.contrib.auth.models  import User
from .forms import *
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import *
from store.models import *
from .middleware import *
from django.core.mail import send_mail
import uuid
from django.utils.decorators import method_decorator
from  django.contrib.auth.decorators import login_required

# Create your views here.

@unauthenticateduser
def register(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        phone = request.POST.get('phone')
        if form.is_valid():
            user_details = form.save()
          
            #creating cstomer object and add it to customer groups
            Customer.objects.create(
                Phone_no=phone,email=user_details.email,
            )
            #adding it to group
            group = Group.objects.get(name='customer')
            user_details.groups.add(group)
            
            password = request.POST['password1']
            #login 
            user = authenticate(request,username=user_details.username,
                        password=password)        
            dj_login(request,user)

             
    context = {'form':form}
    return render(request,'accounts/register.html',context)


@unauthenticateduser
def register_vendor(request):
    form = VendorRegistrationForm()
    if request.method == "POST":
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():


            try:
                #Sending Verifications Mail
                #inactive_user = send_verification_email(request,form) 
                vendor_detials = form.save()
                
                auth_token = str(uuid.uuid4())
                username = request.POST['username']
                email = request.POST['email']
                vendor_trade_name = request.POST['TRADE_NAME']
                vendor_add = request.POST['office_address']
                vendor_supply = request.POST['NATURE_OF_SUPPLY']
                phone_no = request.POST['phone_no']
                name = request.POST['Name']
                passs = request.POST['password1']
                
                #making user variable
                user  = User.objects.get(username=vendor_detials.username)

                
                #creating vendor detials
                Vendor.objects.create(user=user,auth_token=auth_token,Name=name,
                Email=vendor_detials.email,
                phone_no= phone_no,
                trade_name=vendor_trade_name,
                address=vendor_add,
                NATURE_OF_SUPPLY=vendor_supply)

                #adding user to vendor accounts
                group = Group.objects.get(name='vendor')
                vendor_detials.groups.add(group)

                #sending mail for verification
                send_mail_after_registration(email,auth_token)
                return redirect('/token')
                
            except:
                u = User.objects.get(username=vendor_detials.username)
                v = Vendor.objects.get(user=u)
                v.delete()
                u.delete()
                return HttpResponse('<h1>There was error please retry <a href="#" > Back</a> </h1>')
            else:
                return HttpResponse('<h1> 404 UNKOWUNU ERROR .. PLEASE RETRY </h1>')
        
    context = {'form':form}

    return render(request,"accounts/register_vendor.html",context)


def logoutUser(request):
    logout(request)
    return HttpResponse('You have Succecfully logout')

@unauthenticateduser
def Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user_obj = User.objects.filter(username=username).first()
        try:
            vendor = Vendor.objects.get(user=user_obj)
            email = user_obj.email
        
            if not vendor.is_verified :
                messages.success(request, 'Profile is not verified check your mail , we have send the verification link.')
                #creating auth token
                auth_token = str(uuid.uuid4())
                vendor.auth_token = auth_token 
                vendor.save()
                
                #sending mail to the user
                send_mail_after_registration(email,auth_token,)
                return redirect('/accounts/login')
        except:
            pass
        user = authenticate(request,username=username,password=password)
        dj_login(request,user)
        return redirect('/')    
        
    return render(request,'accounts/login.html')  


@login_required(login_url='login')
def vendor_dashboard(request):
    vendor = User.objects.get(username=username)
    print(vendor.id)

    context ={}
    return render(request,'accounts/vendor_dashboard.html',context)
  


def success(request):
    return render(request , 'accounts/success.html')


def token_send(request):
    return render(request , 'accounts/token_send.html')


def verify(request , auth_token):
    try:
        profile_obj = Vendor.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'accounts/error.html')





def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )