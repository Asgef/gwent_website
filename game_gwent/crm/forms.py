from django import forms
from .models import User, Address, Order, OrderItem
from phonenumber_field.formfields import (
    PhoneNumberField as FormPhoneNumberField
)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user_comment']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class UserForm(forms.ModelForm):
    phone_num = FormPhoneNumberField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={'placeholder': '+7'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'phone_num', 'email']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['postal_code', 'region', 'city', 'street', 'house', 'apt']
        widgets = {
            'postal_code': forms.TextInput(attrs={'id': 'id_postal_code'}),
            'region': forms.TextInput(attrs={'id': 'id_region'}),
            'city': forms.TextInput(attrs={'id': 'id_city'}),
            'street': forms.TextInput(attrs={'id': 'id_street'}),
            'house': forms.TextInput(),
            'apt': forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['street'].widget.attrs.update({
            'data-autocomplete-url': '/autocomplete/address/'
        })
