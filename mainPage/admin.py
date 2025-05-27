from django.contrib import admin

from .models import Product,Category, Comment
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'count', 'available', 'rating']
    list_filter = ['available', 'category']
    search_fields = ['name', 'description']
    list_editable = ['price', 'count', 'available']
    readonly_fields = ['rating', 'num_ratings']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'image', 'price')
        }),
        ('Inventory', {
            'fields': ('count', 'available'),
            'description': 'Set count to 0 to mark as unavailable'
        }),
        ('Rating Information', {
            'fields': ('rating', 'num_ratings'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Update availability based on count
        obj.update_availability()
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at', 'has_reply']
    list_filter = ['created_at', 'product']
    search_fields = ['text', 'user__username', 'product__name']
    readonly_fields = ['user', 'product', 'text', 'created_at']
    
    def has_reply(self, obj):
        return bool(obj.reply)
    has_reply.boolean = True
    has_reply.short_description = 'Has Reply'
