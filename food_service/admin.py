from django.contrib import admin

from .models import Food, OrderQuantity, Order


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderQuantity)
class OrderQuantityAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
