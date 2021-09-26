# from django.contrib import admin
#
# from orders.models import Order, Customer, Notification
#
# admin.site.register(Order)
# admin.site.register(Customer)
# admin.site.register(Notification)

from django import forms
from django.contrib import admin

from .models import Order, OrderItem



# class OrderCreateForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'email', 'address',
#                   'postal_code', 'city']



admin.site.register(Order)
admin.site.register(OrderItem)