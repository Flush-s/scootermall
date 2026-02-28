from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, PromoCode


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'total_items', 'total_price', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'session_id']
    inlines = [CartItemInline]
    readonly_fields = ['total_items', 'total_price']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at']
    search_fields = ['cart__id', 'product__name']
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'phone', 'email']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'order_number', 'status', 'created_at', 'updated_at')
        }),
        ('Контактная информация', {
            'fields': ('first_name', 'last_name', 'phone', 'email')
        }),
        ('Адрес доставки', {
            'fields': ('city', 'address', 'zip_code')
        }),
        ('Оплата', {
            'fields': ('total_amount', 'delivery_cost', 'discount', 'promo_code')
        }),
        ('Дополнительно', {
            'fields': ('comment',)
        }),
    )


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'discount_amount', 'is_active', 'valid_from', 'valid_to', 'used_count']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']
