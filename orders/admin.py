from django.contrib import admin

from orders.models import Order, Customer, Notification

admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Notification)