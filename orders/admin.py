from django.contrib import admin

from .models import Order, OrderItem, Delivery


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'order_number',
        'customer',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'order_number',
        'customer__username',
        'phone',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'product',
        'quantity',
        'price',
    )

    search_fields = (
        'order__order_number',
        'product__name',
    )


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'delivery_person',
        'status',
        'current_latitude',
        'current_longitude',
        'assigned_at',
        'delivered_at',
    )

    list_filter = (
        'status',
        'assigned_at',
        'delivered_at',
    )

    search_fields = (
        'order__order_number',
        'delivery_person__username',
    )