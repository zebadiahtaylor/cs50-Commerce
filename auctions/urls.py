from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('auction/<int:auction_id>', views.auction, name='auction'),
    path('bid/<int:auction_id>', views.bid, name='bid'),
    path('sell', views.sell, name='sell'),
    path('my_auctions', views.my_auctions, name='my_auctions'),
    path('categories', views.categories, name='categories'), 
    path('category/<int:category_id>', views.category, name='category'), 
    path('close_auction/<int:auction_id>', views.close_auction, name='close_auction'),
    path('comment/<int:auction_id>', views.comment, name='comment'),
    path('edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('remove_comment/<int:comment_id>', views.remove_comment, name='remove_comment'), 
    path('delete_auction/<int:auction_id>', views.delete_auction, name='delete_auction'),
    path('watchlist', views.watchlist, name='watchlist'), 
    path('add_to_watchlist', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist', views.remove_from_watchlist, name='remove_from_watchlist'),
]
