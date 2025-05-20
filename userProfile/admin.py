from django.contrib import admin
from .models import UserProfile, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'user', 'created_at', 'total_amount', 'is_paid']
    list_filter = ['created_at', 'is_paid']
    search_fields = ['tracking_code', 'user__username', 'user__email']
    inlines = [OrderItemInline]
    readonly_fields = ['tracking_code']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'address']
    search_fields = ['user__username', 'user__email', 'phone_number']
   
