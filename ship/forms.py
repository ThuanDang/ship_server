from django import forms

from ship.models import Account, Customer, Shipper


class CustomerAdminForm(forms.ModelForm):
    account = forms.ModelChoiceField(Account.objects.all().filter(type='customer'))

    class Meta:
        model = Customer
        fields = ['account', 'phone', 'address']


class ShipperAdminForm(forms.ModelForm):
    account = forms.ModelChoiceField(Account.objects.all().filter(type='shipper'))

    class Meta:
        model = Shipper
        fields = ['account', 'phone', 'card_id', 'ratting', 'address']