from django.shortcuts import render

from django.shortcuts import render

from main.models import Cart
from .admin import OrderCreateForm
from .models import OrderItem




def order_create(request, order_created=None):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item["product"],
                                         price=item["price"],
                                         quantity=item["quantity"])
            cart.clear()
            order_created.delay(order.id)
            return render(request,
                          "orders/created.html",
                          {"order": order})
    else:
        form = OrderCreateForm()
    return render(request, "orders/create.html",
                  {"cart": cart, "form": form})
