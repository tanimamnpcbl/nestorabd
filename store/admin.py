from django.contrib import admin

from .models import (
    Category,
    Product,
    Order,
    OrderItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'slug',
        'is_active',
        'created_at'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'category',
        'price',
        'sale_price',
        'stock',
        'is_active'
    ]

    list_filter = [
        'category',
        'is_active'
    ]

    search_fields = [
        'name',
        'sku',
        'author',
        'brand'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = [
        'product_name',
        'price',
        'quantity',
        'subtotal'
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'order_number',
        'name',
        'phone',
        'total',
        'payment_method',
        'payment_status',
        'status',
        'created_at'
    ]

    list_filter = [
        'status',
        'payment_status',
        'payment_method',
        'created_at'
    ]

    search_fields = [
        'order_number',
        'name',
        'phone',
        'email',
        'transaction_id'
    ]

    readonly_fields = [
        'order_number',
        'created_at'
    ]

    inlines = [
        OrderItemInline
    ]