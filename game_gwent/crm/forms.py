from django import forms
from .models import User, Address, Order, OrderItem
from phonenumber_field.modelfields import PhoneNumberField


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class UserForm(forms.ModelForm):
    phone_num = PhoneNumberField(blank=False, region='RU')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'phone_num', 'email']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['region', 'city', 'street', 'house', 'apt', 'postal_code']
        widgets = {
            'region': forms.TextInput(attrs={'id': 'id_region'}),
            'city': forms.TextInput(attrs={'id': 'id_city'}),
            'street': forms.TextInput(attrs={'id': 'id_street'}),
            'house': forms.TextInput(),
            'apt': forms.TextInput(),
            'postal_code': forms.TextInput(attrs={'id': 'id_postal_code'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['street'].widget.attrs.update({
            'data-autocomplete-url': '/autocomplete/address/'
        })

