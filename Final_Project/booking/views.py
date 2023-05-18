from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PropertyFilter, AddProperty
from .models import Listing
from datetime import date, timedelta
from django.db.models import Q

from .models import User, PropertyType

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
            complete_form.save()
            return HttpResponseRedirect(reverse("booking:index"))
        else:
            return render(request, "booking/add.html", {
                "form": form
            })
        
def detail_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if request.method == "GET":
        return render(request, "booking/detail.html", {
            "listing": listing
        })
    
    else:
        return HttpResponseRedirect(reverse("booking:detail", args=[listing.id]))