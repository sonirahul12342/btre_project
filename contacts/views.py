from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from django.contrib.auth.models import User,auth
# Create your views here.
def contact(request):
        try:
                if request.user.is_authenticated :
                        if request.method == 'POST':
                                listing_id=request.POST['listing_id']
                                listing=request.POST['listing']
                                name=request.POST['name']
                                email=request.POST['email']
                                phone=request.POST['phone']
                                message=request.POST['message']
                                user_id=request.POST['user_id']
                                realtor_email=request.POST['realtor_email']
                                #check if user has made enquiury already
                                try:
                                        if request.user.is_authenticated :
                                                user_id=request.user.id
                                                has_contacted= Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
                                                if has_contacted:
                                                        messages.error(request,'you already made a query')
                                                        return redirect('/listings'+listing_id)                            
                                        contact=Contact(listing=listing,listing_id=listing_id,name=name,email=email,phone=phone,message=message,user_id=user_id,realtor_email=realtor_email)
                                        contact.save()
                                        '''send_mail(
                                                'Property Listing Enquiry',
                                                'there has been enquiry for'+listing,
                                                'company@gmail.com',[realtor_email,'checkingemail@gmail.com'],
                                                fail_silently=False
                                        )'''
                                        messages.success(request,'your request is submitted')
                                        return redirect('/listings'+listing_id)
                                except:
                                        if request.user.is_authenticated:
                                                auth.logout(request)
                                        messages.error(request,'Error Exits: we are trying to solve try again later')
                                        return redirect('/listings'+listing_id)
                else:
                        messages.error(request,'You are not logged in. either register yourself or try to login')
                        return redirect('login') 
        except:
                if request.user.is_authenticated:
                        auth.logout(request)
                messages.error(request,'Error Exits: we are trying to solve try again later')
                return redirect('index')