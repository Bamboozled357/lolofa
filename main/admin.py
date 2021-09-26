from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import ProductImage
from main.models import Product, UserProductRelation, Response, Cart


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass


@admin.register(UserProductRelation)
class UserProductRelationAdmin(ModelAdmin):
    pass


@admin.register(Response)
class UserProductRelationAdmin(ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    pass

admin.site.register(ProductImage)
