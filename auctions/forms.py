from django import forms
from .models import Auction, Bid, Category, Comment


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'category', 'description', 'starting_bid']
        widgets = {
            'category' : forms.Select(choices=Category.objects.all(),
                                attrs={'class' : 'form-control'}),
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control'}),
            'starting_bid' : forms.NumberInput(attrs={'step' : .01}),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        labels = {'bid_amount': ""}
        widgets = {
            'bid_amount': forms.NumberInput(attrs={'step' : .01, 'floatformat' : 2})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ""}
        widgets = {
            'text': forms.Textarea(attrs={'class' : 'form-control'})
        }

