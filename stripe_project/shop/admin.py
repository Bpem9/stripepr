from django.contrib import admin
from .models import *


@admin.register(Item)
class ItemModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    list_editable = ('name', 'description', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'list_items', 'total_price')