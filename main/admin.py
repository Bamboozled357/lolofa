from django.contrib import admin
from django.contrib.admin import ModelAdmin

from main.models import Product, UserProductRelation,Response


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass

@admin.register(UserProductRelation)
class UserProductRelationAdmin(ModelAdmin):
    pass

@admin.register(Response)
class UserProductRelationAdmin(ModelAdmin):
    pass