from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', verbose_name='auction',
                        related_name='watchlist')


class Auction(models.Model):
    user = models.ForeignKey(User, 
                        on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.ForeignKey('Category', 
                        verbose_name='category', blank=True, 
                        on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    starting_bid = models.DecimalField(default=1.00,
                        null=True, max_digits=19, decimal_places=2)
    image_url = models.URLField(default=None, 
                        max_length=40000, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Seller: {self.user}. Title: {self.title}. Description: {self.description}. Starting bid: {self.starting_bid}. Image_URL: Deactivated."


class Bid(models.Model):
    auction = models.ForeignKey('Auction', verbose_name='auction',
                        on_delete=models.CASCADE)
    bid_amount = models.DecimalField(null=True, default=.01, max_digits=19, decimal_places=2)
    user = models.ForeignKey(User, verbose_name='user', 
                        on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bid_amount}"


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='user',
                    on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, verbose_name='auction',
                        on_delete=models.CASCADE)
    text = models.CharField(max_length=300, null=True, default="")

    def __str__(self):
        return f'{self.user} says "{self.text}"'