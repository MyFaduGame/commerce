from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django import forms

from .forms import ListingsForm, BidForm
from .models import User, Listings, Categories, Watchlists, Bid


def index(request):
    
    return render(request, "auctions/index.html",{
        "listings": Listings.objects.all(),
        "categories":Categories.objects.all(),
        "bids":list(Bid.objects.values('listings').annotate(price=Max('current_bid')))
        })


def create(request):
    if request.method == "POST":
        form=ListingsForm(request.POST or None)
        if form.is_valid:
            form.save()
            new_listings=Listings.objects.all()
        return render(request, "auctions/index.html",{
            "listings":new_listings
        })
    else:
        form = ListingsForm
        return render(request, "auctions/create.html",{
            "form":form
        })


def detail_view(request, listing_id):
    listing=Listings.objects.get(pk=listing_id)
    form = BidForm()
    if Bid.objects.filter(listings=listing_id).exists():
        bid=Bid.objects.filter(listings=listing).last()
    else:
        bid=Bid.objects.create(current_bid=listing.start_bid, user=listing.user, listings=listing) 
    return render(request, "auctions/detail.html",{
            "listing":listing,
            "form": form,
            "bid":bid
        }) 

@login_required
def bid(request, listing_id):
    listing=get_object_or_404(Listings, pk=listing_id)
    current_bid=Bid.objects.filter(listings=listing_id).last().current_bid
    start_bid=listing.start_bid
    if request.method == "POST":
        form = BidForm(request.POST or None)
        if form.is_valid:
            bid = form.save(commit=False)
            new_bid=form.cleaned_data.get('current_bid')
            bid.user = request.user
            bid.listings = listing
            if new_bid > start_bid and new_bid > current_bid:    
                bid.save()
                return HttpResponseRedirect(reverse('detail_view', args=(listing.id,)))
                        
            else:
                #messages.warning(request, 'Invalid Bid!!')
                messages.add_message(request, messages.WARNING, 'Invalid Bid! Bid must be greater than current price.')
                return HttpResponseRedirect(reverse('detail_view', args=(listing.id,)))
                #return HttpResponseRedirect('/detail/%s' % listing.id)
                    #"message":"Invalid Bid!!!!"
    else:
        form=BidForm()
        return render(request, 'auctions/detail.html',{
            "form":form
        })
     
@login_required
def close_bid(request, listing_id):
    listing=Listings.objects.get(pk=listing_id)
    if listing.user == request.user:
        return HttpResponse("Listing closed!")
    else:
        return HttpResponseRedirect(reverse('detail_view', args=(listing_id,)))
                

@login_required
def watchlist(request, listing_id):
    listing_to_save=Listings.objects.get(pk=listing_id)
    #listing_to_save = get_object_or_404(Listings, pk=listing_id)
    if Watchlists.objects.filter(user=request.user, listings=listing_id).exists():
        exist_listing=Watchlists.objects.get(user=request.user, listings=listing_id)
        exist_listing.listings.remove(listing_to_save)
        messages.info(request, 'Listing removed from Watchlist.')
        #messages.add_message(request, messages.INFO, 'Listing removed from Watchlist.')
        if not exist_listing.listings.all():    #if the list is empty, delete the entire list belongs to that user
            exist_listing.delete()
        return HttpResponseRedirect(reverse('detail_view',args=(listing_to_save.id,)))
    user_list, created = Watchlists.objects.get_or_create(user=request.user)
    user_list.listings.add(listing_to_save)
    messages.success(request, 'Successfully added to your watchlist!')
    return HttpResponseRedirect(reverse('detail_view',args=(listing_to_save.id,)))
        
@login_required
def view_list(request):
    items=Watchlists.objects.all()
    for item in items:
        if item.user == request.user:
            listings=item.listings.all()
            return render(request, "auctions/watchlist.html",{
                "listings":listings,
                "bids":list(Bid.objects.values('listings').annotate(price=Max('current_bid')))
            })
        else:
            return render(request, "auctions/watchlist.html",{
                "message":"(You have not added anything in your watchlist)"
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
