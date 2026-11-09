from django.contrib import admin
from .models import Shop, ShopProduct


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'owner',
        'phone',
        'city',
        'is_open',
        'accepts_orders',
    )

    list_filter = (
        'is_open',
        'accepts_orders',
        'city',
    )

    search_fields = (
        'name',
        'phone',
        'city',
    )


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = (
        'shop',
        'product',
        'price',
        'stock',
        'is_available',
    )

    list_filter = (
        'is_available',
        'shop',
    )

    search_fields = (
        'shop__name',
        'product__name',
        'product__part_number',
    )
