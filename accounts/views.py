from django.shortcuts import render,redirect,render_to_response
from rest_framework.response import Response, responses
from django.contrib import messages
from django.contrib.auth.models import User,auth
from rest_framework.authtoken.models import Token
from contacts.models import Contact
from re import match
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from listings.choices import bedroom_choices,price_choices,state_choices

from django.db.models import Q
from listings.models import Listing
from django.contrib.auth.hashers import make_password,check_password
from users.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from users.backend import EmailOrUsernameModelBackend
from realtor.models import Realtor
from django.core.files.storage import FileSystemStorage
# Create your views here.
def login(request):
    if not request.user.is_authenticated:
            try:
                    if request.method == 'POST':
                        username=request.POST['username']
                        password=request.POST['password']
                        user=auth.authenticate(username=username,password=password)
                        if user is not None:
                                if user.is_active:
                                    
                                        auth.login(request,user)
                                        token,_=Token.objects.get_or_create(user=user)
                                        context={'Authorization': 'Token '+token.key}
                                        
                                        return redirect('dashboard')
                                    
                                else:
                                    messages.error(request,'Account is not Active check your mail')
                                    return redirect('login')
                        else:
                            messages.error(request,'invalid credentials')
                            return redirect('login')
                    else:
                        return render(request,'accounts/login.html')
            except :
                if request.user.is_authenticated:
                    auth.logout(request)
                messages.error(request,'Error Exits: we are trying to solve try again later')
                return redirect('login')
    else:
        messages.error(request,'You are already logged in')
        return redirect('dashboard')
    
def register(request):
    if not request.user.is_authenticated:
        try:
            if request.method == 'POST':
                first_name=request.POST['first_name']
                last_name=request.POST['last_name']
                username=request.POST['username']
                email=request.POST['email']
                phone=request.POST['phone']
                password=request.POST['password']
                password2=request.POST['password2']
                pattern="[a-z]+[A-Z]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+"
                if password == password2:
                    if match(pattern,password):
                            if CustomUser.objects.filter(username=username).exists():
                                messages.error(request,'usernmae exsits')
                                return redirect('register')
                            else:
                                if CustomUser.objects.filter(email=email).exists():
                                    messages.error(request,'email exsits')
                                    return redirect('register')
                                else:
                                    user=CustomUser.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email,phone=phone)
                                    #auth.login(request,user)
                                    #messages.success(request,'you are now logged in')
                                    #return redirect('index')
                                    user.is_active=False
                                    user.save()
                                    current_site = get_current_site(request)
                                    email_subject = 'Activate Your Account'
                                    message_tosend = render_to_string('accounts/activate_account.html', {
                                        'user': user,
                                        'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.id)),
                                        'token': account_activation_token.make_token(user),
                                        
                                    })
                                    send_mail(
                                            email_subject,
                                            message_tosend,'sonirahul12342@gmail.com',[email],
                                            fail_silently=False
                                    )
                                    messages.success(request,'check your email for activating your account')
                                    return redirect('login')
                    else:
                        messages.error(request,'password must contain atleast one uppercase and one digit')
                        return redirect('register')

                else:
                    messages.error(request,'password not match')
                    return redirect('register')
            else:
                return render(request,'accounts/register.html')
        except :
            if request.user.is_authenticated:
                auth.logout(request)
            messages.error(request,'Error Exits: we are trying to solve try again later')
            return redirect('login')
    else:
        messages.error(request,'You are already logged in')
        return redirect('dashboard')

def dashboard(request):
    try:
        token1=Token.objects.get(user_id=request.user.id)
        if Token.objects.filter(user_id=request.user.id).exists():
                    user_contacts=Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
                    context={'contacts':user_contacts,}
                    is_exp=token_expire_handler(token1)
                    if is_exp:
                        auth.logout(request)
                        messages.error(request,'Token expires Login again')
                        return redirect('login')
                    else:
                        return render(request,'accounts/dashboard.html/',context)
        else:
            if request.user.is_authenticated:
                auth.logout(request)
            messages.error(request,'Token Invalid')
            return redirect('login')
    except :
        if request.user.is_authenticated:
            auth.logout(request)
        messages.error(request,'Error Exits: we are trying to solve try again later')
        return redirect('login')

def logout(request):
    try:
        if request.method == 'POST':
            auth.logout(request)
            messages.success(request,'you are logged out')
            return redirect('index')
    except:
        if request.user.is_authenticated:
            auth.logout(request)
        messages.error(request,'Error Exits: we are trying to solve try again later')
        return redirect('index')
def activate_account(request,uidb64,token):
            try:
                uid = force_bytes(urlsafe_base64_decode(uidb64))
                user = CustomUser.objects.get(id=uid)
            except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                user = None
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                #login(request, user)
                messages.success(request,'your account has been activated now you can login')
                return redirect('login')
            else:
                messages.error(request,'Activation link is invalid!')
                return redirect('register')

#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(days=1) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        
    return is_expired



def login_r(request):
            if request.method == 'POST':
                username=request.POST['username']
                password=request.POST['password']
                user=auth.authenticate(username=username,password=password)
                if user is not None:
                        if user.is_active:
                            if user.is_realtor:
                                auth.login(request,user)
                                token,_=Token.objects.get_or_create(user=user)
                                context={'Authorization': 'Token '+token.key}
                                
                                return redirect('dashboard_r')
                            else:
                                messages.error(request,'You are not a Realtor')
                                return redirect('login_r')
                        else:
                            messages.error(request,'Account is not Active check your mail')
                            return redirect('login_r')
                else:
                    messages.error(request,'invalid credentials')
                    return redirect('login_r')
            else:
                return render(request,'accounts/login_realtor.html')
def register_realtor(request):
    if request.method == 'POST':
                first_name=request.POST['first_name']
                last_name=request.POST['last_name']
                username=request.POST['username']
                email=request.POST['email']
                phone=request.POST['phone']
                password=request.POST['password']
                password2=request.POST['password2']
                photo=request.FILES['photo']

                pattern="[a-z]+[A-Z]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+[a-z|A-Z|@|#|0-9]+"
                if password == password2:
                    if match(pattern,password):
                            if CustomUser.objects.filter(username=username).exists():
                                messages.error(request,'usernmae exsits')
                                return redirect('register_realtor')
                            else:
                                if CustomUser.objects.filter(email=email).exists():
                                    messages.error(request,'email exsits')
                                    return redirect('register_realtor')
                                else:
                                                fs=FileSystemStorage()
                                                name=fs.save(photo.name,photo)
                                                user=CustomUser.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email,phone=phone)
                                                user.is_active=False
                                                user.is_realtor=True
                                                user.save()
                                                
                                                user_r=Realtor(name=first_name+last_name,email=email,phone=phone,photo=photo.name,user_id=user.id)
                                                #auth.login(request,user)
                                                #messages.success(request,'you are now logged in')
                                                #return redirect('index')
                                                
                                                

                                                user_r.save()
                                                current_site = get_current_site(request)
                                                email_subject = 'Activate Your Account'
                                                message_tosend = render_to_string('accounts/activate_account.html', {
                                                    'user': user,
                                                    'domain': current_site.domain,
                                                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                                                    'token': account_activation_token.make_token(user),
                                                    
                                                    
                                                })
                                                send_mail(
                                                        email_subject,
                                                        message_tosend,'sonirahul12342@gmail.com',[email],
                                                        fail_silently=False
                                                )
                                                messages.success(request,'check your email for activating your account')
                                                return redirect('login_r')
                    else:
                        messages.error(request,'password must contain atleast one uppercase and one digit')
                        return redirect('register_realtor')

                else:
                    messages.error(request,'password not match')
                    return redirect('register_realtor')
    else:
                return render(request,'accounts/register_realtor.html')
  

    

def register_listing(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_realtor:
            user_id=request.POST['user_id']
            realtor_email=request.POST['realtor_email']
            realtor_name=Realtor.objects.get(name=realtor_email)
     
            title=request.POST['title']
            address=request.POST['address']
            city=request.POST['city']
            state=request.POST['state']
            zipcode=request.POST['zipcode']
            description=request.POST['description']
            price=request.POST['price']
            bedrooms=request.POST['bedrooms']
            bathrooms=request.POST['bathrooms']
            garage=request.POST['garaze']
            sqft=request.POST['sqft']
            lot_size=request.POST['lot_size']
            photo_main=request.FILES['photo_main']
            photo_1=request.FILES['photo_1']
            
            fs=FileSystemStorage()
            fs.save(photo_main.name,photo_main)
            fs.save(photo_1.name,photo_1)
            
            register_listing=Listing(title=title,address=address,city=city,state=state,zipcode=zipcode,description=description,price=price,bedrooms=bedrooms
                                        ,bathrooms=bathrooms,garage=garage,sqft=sqft,lot_size=lot_size,photo_main=photo_main,photo_1=photo_1,user_id=request.user.id,realtor=realtor_name
            )
            register_listing.save()
            return redirect('register_listing')
    else:
        return render(request,'accounts/register_listing.html')
def register_r(request):
    return render(request,'accounts/register_realtor.html')

def login_realtor(request):
    return render(request,'accounts/login_realtor.html')

def check_realtor(username=None,password=None):
    if username is None:
        return None

    user= Realtor.objects.filter(username=username)

    if check_password(password,user.password):
        return user
    if not user:
        return None
def dashboard_r(request):
        '''try:'''
        token1=Token.objects.get(user_id=request.user.id)
        if Token.objects.filter(user_id=request.user.id).exists():
                    
                    realtor_listings=Listing.objects.order_by('-list_date').filter(user_id=request.user.id)
                    print(realtor_listings)
                    coming_inquiry=Contact.objects.order_by('-contact_date').filter(realtor_email=request.user.email)
                    print(coming_inquiry)
                    context={'listings_r':realtor_listings,'state_choices':state_choices,'inquries_r':coming_inquiry}
                    is_exp=token_expire_handler(token1)
                    if is_exp:
                        auth.logout(request)
                        messages.error(request,'Token expires Login again')
                        return redirect('login')
                    else:
                        return render(request,'accounts/dashboard_r.html/',context)
        else:
            if request.user.is_authenticated:
                auth.logout(request)
            messages.error(request,'Token Invalid')
            return redirect('login_r')
        '''except :
        if request.user.is_authenticated:
            auth.logout(request)
        messages.error(request,'Error Exits: we are trying to solve try again later')
        return redirect('login_r')'''