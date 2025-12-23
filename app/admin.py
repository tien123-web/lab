from django.contrib import admin
from .models import *

# Đăng ký các model không cần custom
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# Sử dụng decorator cho các model cần custom
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete', 'payment_method', 'payment_status', 'get_cart_total')
    list_filter = ('complete', 'payment_status', 'payment_method')
    search_fields = ('id', 'customer__username', 'transaction_id')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_method', 'amount', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'order__id')