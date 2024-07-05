from django.contrib import admin, messages
from django import forms

from django.core.exceptions import ValidationError

from .models import Order, User, Address, OrderItem


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        address_instance = Address(**cleaned_data)
        try:
            address_instance.clean()  # Вызов валидации модели
        except ValidationError as e:
            if self.request:
                messages.add_message(self.request, messages.ERROR, str(e))
            raise

class AddressAdmin(admin.ModelAdmin):
    form = AddressForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'address_display', 'total_price', 'paid', 'created_at')
    inlines = [OrderItemInline]

    def address_display(self, obj):
        return f"{obj.address.street}, {obj.address.city}, {obj.address.region}, {obj.address.postal_code}"
    address_display.short_description = 'Address'

admin.site.register(User)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)