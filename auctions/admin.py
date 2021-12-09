from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Auction, Bid, Category, Comment

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


class AuctionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category',
                'description', 'starting_bid', 'active')


class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "bid_amount", "user")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction', 'text')


admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)