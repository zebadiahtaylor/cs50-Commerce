from .models import Auction, Bid, Comment, User
from django.db.models import Max



def has_bids(auction):
    """
    Returns True if others have bid on the item.
    TODO: Throws TypeError if user not logged in
    """
    # auction = Auction.objects.get(id=auction)
    has_bids = False

    try:
        current_bid = Bid.objects.filter(auction=auction).aggregate(Max('bid_amount'))
        if current_bid['bid_amount__max']:              
            has_bids = True

    except Bid.DoesNotExist:
        pass

    return has_bids


def has_high_bid(user, auction):
    """
    Returns True if User has highest bid.
    """
    try:
        max_bid = Bid.objects.filter(auction=auction).aggregate(max_bid = Max('bid_amount'))
        user_high_bid = Bid.objects.filter(auction=auction, user=user).aggregate(user_bid = Max('bid_amount'))
        if user_high_bid['user_bid'] is not None and max_bid['max_bid'] == user_high_bid['user_bid']:
            return True
        else:
            return False

    except Bid.DoesNotExist:
        return False


def is_users_auction(user, auction):
    """
    Returns True if the user is the owner of the auction.
    """
    auction = Auction.objects.get(id=auction)
    is_users_auction = False

    if auction.user == user:
        is_users_auction = True

    return is_users_auction


def is_watched(user, auction):
    user = User.objects.get(username=user)
    watchlist = user.watchlist.all()

    is_watched = False
    for item in watchlist: 
        if auction == item.id:
            is_watched = True

    return is_watched

def return_active_auctions():
    auctions = Auction.objects.all()
    auctions = [auction for auction in auctions if auction.active]
    for auction in auctions:
        auction.current_bid = return_highest_bid(auction.id)

    return auctions


def return_highest_bid(auction):
    auction_object = Auction.objects.get(id=auction)
    current_bid = auction_object.starting_bid

    try:
        max_bid = Bid.objects.filter(auction=auction).aggregate(max_bid = Max('bid_amount'))
        if max_bid['max_bid']:
            current_bid = max_bid['max_bid']
            return current_bid

    except Bid.DoesNotExist:
        pass

    return current_bid


def return_all_comments(auction):
    comments = Comment.objects.filter(auction=auction)
    return comments


