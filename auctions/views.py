from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    # Get all categories & listings 
    listing = Listing.objects.filter(is_active=True)
    categorys = Category.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listing,
        "categorys": categorys
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    # Gather info if the route was reached after submitting create form
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['image_url']
        starting_bid = request.POST['starting_bid']
        category = request.POST['category']
        creator = request.user
        
        # Create the new listing object and save it
        new_listing = Listing.objects.create(
            title = title,
            description = description,
            image_url = image_url,
            starting_bid = starting_bid,
            category = Category.objects.get(category=category),
            creator = creator)
        new_listing.save()
        
        return HttpResponseRedirect(reverse("index"))
    
    categorys = Category.objects.all()
    return render(request, "auctions/create_listing.html", {
        "categorys": categorys
    })


def categories(request):
    # Get all categories
    categorys = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "categorys": categorys
    })


def listing(request, listing_id):
    # Get the listing requested with id
    listing = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing
    })


def category_listings(request, category_id):
    # Get the category requested with id
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category_id)

    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })