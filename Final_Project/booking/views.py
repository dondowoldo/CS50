from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PropertyFilter, AddProperty, PostComment, MakeBooking
from .models import Listing, User, PropertyType, AvailableDate, Comment
from datetime import date, timedelta
from django.db.models import Q
from django.conf import settings
import folium
import geocoder
from django.core.paginator import Paginator


# gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("booking:index"))
        else:
            return render(request, "booking/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "booking/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("booking:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "booking/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "booking/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("booking:index"))
    else:
        return render(request, "booking/register.html")


def index(request):
    if request.method =="GET":
        return render(request, "booking/index.html", {
            "form": PropertyFilter(),
            "listings": Listing.objects.all()
        })
    else:
        if  request.POST.get("filter"):
            form = PropertyFilter(request.POST)  
            if form.is_valid():               
                
                ## QUERING DB FOR FILTERS IF SPECIFIED BY USER
                filters = form.cleaned_data
                query = Q()
            
                if filters["title"] is not None:
                    query &= Q(title__contains=filters["title"])
                
                if filters["type"] is not None:
                    query &= Q(type=filters["type"])
                
                if filters["price_per_night"]:
                    query &= Q(price_per_night__lte=filters["price_per_night"])

                if filters["availability_from"]:
                    query &= Q(availability_from__lte=filters["availability_from"])

                if filters["availability_to"]:
                    query &= Q(availability_to__gte=filters["availability_to"])

                filtered = Listing.objects.filter(query)                

                return render(request, "booking/index.html", {
                "form": form,
                "listings": filtered
                })
            else:
                return render(request, "booking/index.html", {
                "form": form
                })       
        elif request.POST.get("reset"):
            return HttpResponseRedirect(reverse("booking:index"))
        
@login_required(login_url='booking:login')
def addProperty(request):
    if request.method == "GET":
        return render(request, "booking/add.html", {
            "form": AddProperty()
        })
    else:
        form = AddProperty(request.POST)
        if form.is_valid():
            complete_form = form.save(commit=False)
            complete_form.creator = request.user
            geocode = geocoder.osm(complete_form.location)
            complete_form.geolat = geocode.lat
            complete_form.geolng = geocode.lng    
            complete_form.save()
            
            # Get all available dates from list and check if dates are already in db. If not = create, if so = assign to an instance and save relationship
            date_list = get_initial_dates(complete_form.availability_from, complete_form.availability_to)
            for mydate in date_list:
                date_entry, created = AvailableDate.objects.get_or_create(date=mydate)
                complete_form.available_dates.add(date_entry)

            return HttpResponseRedirect(reverse("booking:index"))
        else:
            return render(request, "booking/add.html", {
                "form": form
            })
        
def detail_view(request, listing_id):
    submitted = False   # Check if user clicked on view on map button and if so, render map instead of image

    listing = Listing.objects.get(id=listing_id)
    
    # Folium map Setup
    geomap = folium.Map([listing.geolat, listing.geolng], zoom_start=10)
    folium.Marker([listing.geolat, listing.geolng]).add_to(geomap)
    geomap = geomap._repr_html_()
    
    if request.method == "GET":      
        return render(request, "booking/detail.html", {
            "listing": listing,
            "geomap": geomap,
            "submitted": submitted
        })
    else:
        if request.POST.get("submitted"):
            submitted = True   
            return render(request, "booking/detail.html", {
            "listing": listing,
            "geomap": geomap,
            "submitted": submitted
        })
        elif request.POST.get("book"):
            return HttpResponseRedirect(reverse("booking:book", args=[listing.id]))              
        else:
            return HttpResponseRedirect(reverse("booking:detail", args=[listing.id]))
    

def comments_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments_desc = Comment.objects.filter(listing__id=listing_id).order_by("-timestamp")
    
    #   Paginator Setup
    paginator = Paginator(comments_desc, 4)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    comment_form = PostComment()

    if request.method == "GET":
        return render(request, "booking/comments.html", {
            "listing": listing,
            "comments": comments,
            "comment_form": comment_form
        })

    else:
        if request.POST.get("sub_comment"):
            comment_form = PostComment(request.POST)
            if comment_form.is_valid():
                complete_comment = comment_form.save(commit=False)
                complete_comment.user = request.user
                complete_comment.listing = listing
                complete_comment.save()
                return HttpResponseRedirect(reverse("booking:comments", args=[listing.id])) 
            else: 
                return render(request, "booking/comments.html", {
                    "listing_id": listing.id,
                    "comment_form": comment_form,
                    "comments": comments,
                    "listing": listing
                    })   
        else: 
            return HttpResponseRedirect(reverse("booking:comments", args=[listing.id]))  



def book_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    form = MakeBooking()

    if request.method == "GET":
        return render(request, "booking/book.html", {
            "listing": listing,
            "form": form
        })
    
    else:
        form = MakeBooking(request.POST)
        return HttpResponseRedirect(reverse("booking:index"))


## Helper func that gets 2 dates and returns a list of all dates in interval

def get_initial_dates(start_date, end_date):
    available_dates =  []
    available_dates.append(start_date)
    new_date = start_date
  
    for date in range((end_date - start_date + timedelta(days=1)).days):
        if new_date == end_date:
            return available_dates
        else:
            new_date += timedelta(days=1)
            available_dates.append(new_date)