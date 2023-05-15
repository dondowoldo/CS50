from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PropertyFilter

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
        })
    else:
        if  request.POST.get("filter"):
            form = PropertyFilter(request.POST)  
            if form.is_valid():               
                filters = form.cleaned_data
                return render(request, "booking/index.html", {
                
                "type": filters["type"],
                "maxprice": filters["price_per_day"],
                "avlbl_from": filters["availability_from"],
                "avlbl_to": filters["availability_to"],
                "form": form
                })
            else:
                return render(request, "booking/index.html", {
                "form": form
                })       
        elif request.POST.get("reset"):
            return HttpResponseRedirect(reverse("booking:index"))
        

