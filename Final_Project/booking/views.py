from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PropertyFilter, AddProperty, PostComment, MakeBooking, EditProperty
from .models import Listing, User, PropertyType, AvailableDate, Comment, Booking
from datetime import date, timedelta, datetime
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
            
                if filters["location"] is not None:
                    query &= Q(location__contains=filters["location"])
                
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
    available_dates = get_available_dates(listing_id) # Retrieve still avlbl dates of particular listing
    form = MakeBooking(available_dates)
    quote_submitted = False

    if request.method == "GET":
        return render(request, "booking/book.html", {
            "listing": listing,
            "form": form
        })
    
    else:
        form = MakeBooking(available_dates, request.POST)
        if request.POST.get("quote"):
            
            startdate_obj = datetime.strptime(request.POST["startdate"], "%Y-%m-%d").date()
            enddate_obj= datetime.strptime(request.POST["enddate"], "%Y-%m-%d").date()
            selected_dates = get_initial_dates(startdate_obj, enddate_obj) 
            unavailable = get_unavailable_dates(selected_dates, available_dates)

            duration = len(selected_dates)
            price_total = listing.price_per_night * duration

            if form.is_valid():
                quote_submitted = True
                return render(request, "booking/book.html", {
                    "listing": listing,
                    "form": form,
                    "quoted": quote_submitted,
                    "selected_dates": selected_dates,
                    "duration": duration,
                    "startdate": startdate_obj,
                    "enddate": enddate_obj,
                    "price_total": price_total,
                    "unavailable": unavailable
                })
            else:
                return render(request, "booking/book.html", {
                    "listing": listing,
                    "form": form,
                })
        elif    request.POST.get("book"):
                startdate_obj = datetime.strptime(request.POST["startdate"], "%Y-%m-%d").date()
                enddate_obj= datetime.strptime(request.POST["enddate"], "%Y-%m-%d").date()
                selected_dates = get_initial_dates(startdate_obj, enddate_obj) 
                unavailable = get_unavailable_dates(selected_dates, available_dates)
                duration = len(selected_dates)
                price_total = listing.price_per_night * duration

                if not unavailable and form.is_valid():
                    for date in selected_dates:
                        dateobj = AvailableDate.objects.get(availability__id=listing_id, date=date)
                        listing.available_dates.remove(dateobj)
                    listing.save()

                    complete_form = form.save(commit=False)
                    complete_form.user = request.user
                    complete_form.listing = listing
                    complete_form.total_price = price_total
                    complete_form.save()

                    return HttpResponseRedirect(reverse("booking:index"))
                else:
                    return render(request, "booking/book.html", {
                        "listing": listing,
                        "form": form,
                        "quoted": quote_submitted,
                        "selected_dates": selected_dates,
                        "duration": duration,
                        "startdate": startdate_obj,
                        "enddate": enddate_obj,
                        "price_total": price_total,
                        "unavailable": unavailable
                    })

@login_required(login_url='booking:login')
def my_properties_view(request):
    return render(request, "booking/my_properties.html", {
        "listings": Listing.objects.filter(creator=request.user)
    })


@login_required(login_url='booking:login')
def edit_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bookings = Booking.objects.filter(listing=listing)
    unauthorised = False

    form = EditProperty({
        "type": listing.type,
        "title": listing.title,
        "title": listing.title,
        "price_per_night": listing.price_per_night,
        "imageurl": listing.imageurl,
        "location": listing.location,
        # "availability_from": listing.availability_from,
        # "availability_to": listing.availability_to,
        "description": listing.description
    })

    if not request.user == listing.creator:
        unauthorised = True

    if request.method == "GET":
        return render(request, "booking/edit_listing.html",{
            "unauthorised": unauthorised,
            "listing": listing,
            "form": form

        })
    
    else:
        return HttpResponseRedirect(reverse('booking:detail', args=[listing.id]))


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



## Helper function to get all datetime objects stored in db as available_dates
def get_available_dates(listing_id):
    listing_avlbl_dates = Listing.objects.get(id=listing_id).available_dates.all().order_by('date')
    available_dates = []

    for avlbl_date in listing_avlbl_dates:
        available_dates.append(AvailableDate.objects.get(date=avlbl_date.date))
	
    return available_dates

## Helper function to get all dates that user selected and are no longer available
def get_unavailable_dates(selected_dates, available_dates):
    unavailable = []

    for date in selected_dates:
        if any(date == available_date.date for available_date in available_dates):
            continue
        unavailable.append(date)
    return unavailable