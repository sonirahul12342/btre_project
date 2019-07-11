from django.shortcuts import render,get_object_or_404,redirect
from .models import Listing
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from listings.choices import bedroom_choices,price_choices,state_choices
from django.contrib import messages
from django.contrib.auth.models import User,auth
def index(request):
    try:
        listings=Listing.objects.order_by('-list_date').filter(is_published=True)
        paginator=Paginator(listings,6)
        page=request.GET.get('page')
        paged_listings=paginator.get_page(page)
        context= {'listings':paged_listings}
        return render(request,'listings/listings.html',context)
    except:
        messages.error(request,'WE are trying to solve the issue')
        return render(request,'listings/listing.html')  
def listing(request,listing_id ):
    try:
        listing=get_object_or_404(Listing,pk=listing_id)
        context={'listing':listing}
        return render(request,'listings/listing.html',context) 
    except:
        messages.error(request,'listing is not available')
        return redirect('listings') 
def search(request):
    queryset_list=Listing.objects.order_by('-list_date')
    #keyword
    if 'keywords' in request.GET:
        keywords=request.GET['keywords']
        if keywords:
            queryset_list=queryset_list.filter(description__icontains=keywords)
    #city
    if 'city' in request.GET:
        city=request.GET['city']
        if city:
            queryset_list=queryset_list.filter(city__iexact=city)
    #state
    if 'state' in request.GET:
        state=request.GET['state']
        if state:
            queryset_list=queryset_list.filter(state__iexact=state)
    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms=request.GET['bedrooms']
        if bedrooms:
            queryset_list=queryset_list.filter(bedrooms__lte=bedrooms)
    #max rpice
    if 'price' in request.GET:
        price=request.GET['price']
        if price:
            queryset_list=queryset_list.filter(price__lte=price)
    context={'state_choices':state_choices,'price_choices':price_choices,
    'bedroom_choices':bedroom_choices,'listings':queryset_list,'values':request.GET
    }

    return render(request,'listings/search.html',context)