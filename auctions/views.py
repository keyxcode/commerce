from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    # Get all categories & listings 
    listings = Listing.objects.filter(is_active=True).order_by('-id')
    categorys = Category.objects.all().order_by('category')

    # # Update all listings' current price in case of any mistmatch
    # for l in listings:
    #     current_bid = l.current_bid.first()
    #     if current_bid is not None:
    #         l.current_price = current_bid.value
    #         l.save()

    return render(request, "auctions/index.html", {
        "listings": listings,
        "categorys": categorys,
        "status": "Active"
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
    # If the route was reached by POST
    if request.method == "POST":
        # Gather info
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
        
        return HttpResponseRedirect(reverse("listing", args=(new_listing.id,)))
    
    # Return the create listing form if the route was reached by GET
    categorys = Category.objects.all().order_by('category')
    return render(request, "auctions/create_listing.html", {
        "categorys": categorys
    })


def listing(request, listing_id):
    # Get the listing & comments with the provided id
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing).order_by('-id')
    added = Watchlist.objects.filter(listing=listing_id, watcher=request.user)

    # If the route was reached by POST
    if request.method == "POST":

        # If the user is not authenticated, can't do anything
        if request.user.is_anonymous:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "message": "Please log in to continue.",
                "type"  : "warning",
                "added": added
            })

        # If this is a comment submission request
        content = request.POST.get("content", None)
        if content is not None:
            # If comment is empty, render warning
            if content == "":
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "message": "Comments can not be empty",
                    "type": "warning",
                    "added": added
                })

            # If comment is valid, save it to model
            comment = Comment.objects.create(
                content=content,
                commenter=request.user,
                listing=listing
            )
            comment.save()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "message": "Comment successfully posted.",
                "type": "success",
                "added": added
            })

        # If this is a bid sumission request,
        bid_value = request.POST.get("bid_value", None)
        if bid_value is not None:
            # Check if the listing's creator is making a bid:
            if request.user == listing.creator:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "message": "You can not bid on your own listing.",
                    "type": "warning",
                    "added": added
                })

            # Convert the new bid value to number
            try:
                bid_value = float(bid_value)
            # Render error if the new bid is not a number
            except:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "message": "Please input a numerical bidding value.",
                    "type": "warning",
                    "added": added
                })

            # Get the current bid info, if avail, for comparison
            try:
                current_bid = listing.current_bid.first()
            except:
                current_bid = None
            
            # If a current bid exists, get the value and delete it
            if current_bid is not None:
                current_value = current_bid.value
                # Error if bid value < current bid
                if bid_value < current_value: 
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "comments": comments,
                        "message": "Please bid higher than the current bid.",
                        "type": "warning",
                        "added": added
                    })
                # Else, delete the current bid if the new bid is qualified
                current_bid.delete()

            # Error if bid value < starting bid
            elif bid_value < listing.starting_bid:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "message": "Please bid at least the starting amount.",
                    "type": "warning",
                    "added": added
                })
        
            # If passed all the above, register new bid
            current_bid = Bid.objects.create(
                value=bid_value,
                bidder=request.user,
                listing=listing
            )
            current_bid.save()

            # Update listing price and num bids
            listing.current_price = current_bid.value
            listing.num_bids +=1
            listing.save()

            # Success alert
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "message": "Bid successfully placed.",
                "type": "success",
                "added": added
            })
    
    # If the route was reached by GET, render the page
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "added": added
    })


def category_listings(request, category_id):
    # Get the category requested with id
    category = Category.objects.get(pk=category_id)
    categorys = Category.objects.all().order_by('category')
    listings = Listing.objects.filter(category=category_id).order_by('-id')

    return render(request, "auctions/index.html", {
        "categorys": categorys,
        "category": category,
        "listings": listings,
    })


def close_listing(request, listing_id):
    # Get the listing requested with id
    listing = Listing.objects.get(pk=listing_id)

    # Get the current highest bidder for this listing
    bid = Bid.objects.get(listing=listing)

    listing.is_active = False
    listing.winner = bid.bidder
    listing.save()

    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def past_listings(request):
    # Get all categories & listings 
    listings = Listing.objects.filter(is_active=False).order_by('-id')
    categorys = Category.objects.all().order_by('category')

    return render(request, "auctions/index.html", {
        "listings": listings,
        "categorys": categorys,
        "status": "Past"
    })


def watchlist(request, listing_id="None"):
    # If this route was reached by POST
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        
        added = Watchlist.objects.filter(listing=listing_id, watcher=request.user)
        if added:
            watchlist = Watchlist.objects.get(listing=listing, watcher=request.user)
            watchlist.delete()
        else:
            watchlist = Watchlist.objects.create(
                listing=listing,
                watcher = request.user
            )
            watchlist.save()    

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


    # If this route was reached by GET
    watchlists = Watchlist.objects.filter(watcher=request.user).order_by('-id')
    if watchlists:
        listings = map(lambda x: x.listing, watchlists)
    else:
        listings = None
    categorys = Category.objects.all().order_by('category')

    return render(request, "auctions/index.html", {
        "listings": listings,
        "categorys": categorys,
        "status": "Watched"
    })