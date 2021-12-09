from django import forms

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from decimal import Decimal

from .forms import AuctionForm, BidForm, CommentForm
from .models import User, Auction, Bid, Category, Comment
from .utils import has_bids, has_high_bid, is_users_auction, is_watched, return_active_auctions, return_all_comments, return_highest_bid 




def index(request):
    return render(request, "auctions/index.html", {
            "auctions": return_active_auctions()
    })


def auction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    is_users = is_users_auction(request.user, auction_id)

    has_won = has_high_bid(request.user, auction_id)
    message = ""
    if has_won:
        message = "You have won this auction!"

    auction.is_watched = is_watched(request.user, auction_id)
    if auction.is_watched:
        auction.watch_text = "Remove from Watchlist"
    else:
        auction.watch_text = "Add to Watchlist"

    # Determines minimum bid
    auction.current_bid = return_highest_bid(auction_id)
    if has_bids(auction_id): 
        auction.min_bid = auction.current_bid + round(Decimal(f".01"), 2)
    else: 
        auction.min_bid = auction.current_bid
    
    # Subclass allows setting min_bid. 
    class CurrentBidForm(BidForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['bid_amount'].widget.attrs['min'] = auction.min_bid

    bidform = CurrentBidForm(initial = {'bid_amount': auction.current_bid})

    commentform = CommentForm()
    comments = return_all_comments(auction_id)

    return render(request, 'auctions/auction.html', {
        'auction': auction,
        'bidform': bidform, 
        'is_users': is_users,
        'comments': comments,
        'commentform': commentform,
        'has_won': has_won,
        'message': message
    })


def bid(request, auction_id):
    if request.method == "POST":
        form = BidForm(data=request.POST)

        if form.is_valid():
            bid = form.cleaned_data['bid_amount'],
            new_bid =  Bid.objects.create(
                auction = Auction.objects.get(pk=auction_id),
                user = request.user,
                bid_amount = bid[0]
            )

            message = 'You have successfully made a bid on the item.'
        else: 
            message = 'Apologies, there was an error. Make sure to sign in and try again.'


        return render(request, 'auctions/index.html', {
            'auctions': return_active_auctions(), 
            'message' : message
        })
    else:
        return HttpResponseRedirect(reverse('index.html'))
    


def categories(request):
    categories = Category.objects.order_by('name')
    return render(request, 'auctions/categories.html', {
            'categories': categories
    })


def category(request, category_id):
    category = Category.objects.filter(id=category_id)
    auctions = Auction.objects.filter(category=category[0])
    for auction in auctions:
        auction.current_bid = return_highest_bid(auction.id)
    return render(request, 'auctions/category.html', {
        'auctions':auctions,
        'category': category[0]
    })


@login_required
def close_auction(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        auction.active = False
        auction.save()
        message = "Your auction has been closed. An email will be sent to you and the buyer with further instructions."
        return render(request, "auctions/index.html", {
                'auctions': return_active_auctions(),
                'message': message
        })


def comment(request, auction_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        new_comment = Comment.objects.create(
            auction = Auction.objects.get(pk=auction_id),
            user = request.user,
            text = text
        )
    return render(request, "auctions/index.html", {
        'auctions': return_active_auctions(),
        'message': "Your comment has been posted."
    })


def delete_auction(request, auction_id):
    if request.method == "POST":
        if is_users_auction(request.user, auction_id):
            Auction.objects.get(id=auction_id).delete()
            message = "Your auction has been deleted."

        else:
            message = "You do not have permission to delete this auction."
        auctions = Auction.objects.all()
        for auction in auctions:
            auction.current_bid = return_highest_bid(auction.id)

        return render(request, "auctions/index.html", {
                'auctions': return_active_auctions(),
                'message': message
        })
    else:
        return HttpResponseRedirect(reverse("index"))



def my_auctions(request):
    if not request.user.is_anonymous:
        auctions = Auction.objects.filter(user=request.user)
        for auction in auctions:
            auction.current_bid = return_highest_bid(auction.id)

        return render(request, "auctions/my_auctions.html", {
                "auctions":auctions
        })
    else:
        return render(request, 'auctions/index.html', {
            "message": "Log in to view your auctions"
        })


def sell(request):
    if request.method == "POST":
        form = AuctionForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"],
            category = form.cleaned_data["category"],
            description = form.cleaned_data["description"],
            starting_bid = form.cleaned_data["starting_bid"],
            image_url = request.POST["image_url"]
            new_auction =  Auction.objects.create(
                user = request.user,
                title = title[0],
                category = Category.objects.get(name=category[0]),
                description = description[0],
                starting_bid = float(starting_bid[0]),
                image_url = image_url
            )
            
            message = 'Your item was listed successfully. Click "My Auctions" to view it.'

        else:
            message = 'Apologies, but the information could not be validated. Please consider changes and try again.'

        return render(request, "auctions/index.html", {
                'auctions': return_active_auctions(),
                "message": message
        })

    else:
        form = AuctionForm()
        return render(request, 'auctions/sell.html', {
            'form' : form,
        })


def watchlist(request):
    if not request.user.is_anonymous:
        watchlist = request.user.watchlist.all()
        for item in watchlist:
            item.current_bid = return_highest_bid(item.id)
        return render(request, 'auctions/watchlist.html', {
        'auctions' : watchlist
    })
    else:
        return render(request, 'auctions/index.html', {
            "auctions": return_active_auctions(),
            "message": "Log in to view your watchlist"
        })


def add_to_watchlist(request):
    if not request.user.is_anonymous:
        request.user.watchlist.add(request.POST["watchlist"])

        watchlist = request.user.watchlist.all()
        for item in watchlist:
            item.current_bid = return_highest_bid(item.id)
        return render(request, 'auctions/watchlist.html', {
        'auctions' : watchlist,
        "message" : "The auction was successfully added to your Watchlist."
    })

    else: 
        return HttpResponseRedirect(reverse, 'index.html')


def remove_from_watchlist(request):
    if not request.user.is_anonymous:
        request.user.watchlist.remove(request.POST["watchlist"])
        auctions = Auction.objects.all()
        for auction in auctions:
            auction.current_bid = return_highest_bid(auction.id)

        return render(request, 'auctions/index.html', {
            "auctions" : auctions,
            "message" : "The auction was successfully removed from your Watchlist."
        })

    else:
        return HttpResponseRedirect(reverse, 'index.html')


"""editing (not required by cs50 as of July 27th, 2021) """

def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment.text = form.cleaned_data['text']
        comment.save(update_fields=['text'])
        message = "Your comment has been updated."
        return render(request, "auctions/index.html", {
                'auctions': return_active_auctions(),
                'message': message
        })

    else:
        return render(request, 'auctions/index.html', {
            "message": "There was an error in updating your comment.",
            'auctions': return_active_auctions()
        })


def remove_comment(request, comment_id):
    if not request.user.is_anonymous:
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
            message = "Your comment has been deleted."
            return render(request, "auctions/index.html", {
                'auctions': return_active_auctions(),
                'message': message
        })
        
        
        Comment.objects.get(id=comment_id).delete()
        message = "Your comment has been deleted."



"""login, logout, register"""

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
