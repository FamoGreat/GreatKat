from django.contrib import admin
from .models import Order, OrderProduct, Payment


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'order_note', 'order_total', 'order_status', 'is_ordered')
    list_filter = ('order_status',)
    search_fields = ('order_number', 'first_name', 'last_name')
    list_per_page = 20
    ordering = ('-created_at',)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'product', 'quantity', 'product_price', 'ordered')
    list_filter = ('ordered',)
    search_fields = ('order__order_number', 'user__first_name', 'user__last_name', 'product__product_name')
    list_per_page = 20
    ordering = ('-created_at',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('payment_id', 'user__first_name', 'user__last_name')
    list_per_page = 20
    ordering = ('-created_at',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment, PaymentAdmin)
