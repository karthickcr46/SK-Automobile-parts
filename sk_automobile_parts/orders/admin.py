from django.contrib import admin
from .models import Order, OrderItem, DeliveryLocation, DeliveryPartner


@admin.register(DeliveryPartner)
class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "vehicle_number",
        "is_available",
    )

    list_filter = ("is_available",)

    search_fields = (
        "name",
        "phone",
        "email",
        "vehicle_number",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "delivery_partner",
        "total_amount",
        "payment_method",
        "payment_status",
        "order_status",
        "created_at",
    )

    list_filter = (
        "order_status",
        "payment_status",
        "payment_method",
        "delivery_partner",
    )

    search_fields = (
        "customer__name",
        "customer__phone",
        "delivery_partner__name",
        "delivery_partner__phone",
    )

    list_editable = (
        "delivery_partner",
        "order_status",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )


@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "latitude",
        "longitude",
        "accuracy",
        "is_active",
        "updated_at",
    )

    list_filter = ("is_active",)