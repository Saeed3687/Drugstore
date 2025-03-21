from django.contrib import admin

from .models import Product,Category
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_count')

    def product_count(self, obj):
        return obj.products.count()  # Count products in this category

    product_count.short_description = 'Number of Products'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'num_ratings')
    search_fields = ('name',)
    list_filter = ('price', 'rating')
    ordering = ('-rating',)  # Sort by highest rating
