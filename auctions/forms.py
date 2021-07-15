from django.forms import ModelForm, Textarea
from django import forms
from .models import Listings, Categories, Bid
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class ListingsForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = "__all__"
        labels={
            'start_bid':_('Starting Price'),
            'image':_('URL')
        }
        widgets={
            'description': Textarea(attrs={'cols':40, 'rows':5})
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["current_bid"]
        labels={
            'current_bid':_('Value Offer')
        }
        error_messages = {
            'current_bid':{
                'blank':'Sorry, cannot be blank',
                'null':'No null allowed'

            },
        }

  