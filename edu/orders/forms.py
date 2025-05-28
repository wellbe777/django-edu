from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['user', 'created', 'updated', 'paid', 'braintree_id', 'coupon', 'discount']
