from django.contrib import admin

from .models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'num_ratings')
    search_fields = ('name',)
    list_filter = ('price', 'rating')
    ordering = ('-rating',)  # Sort by highest rating
