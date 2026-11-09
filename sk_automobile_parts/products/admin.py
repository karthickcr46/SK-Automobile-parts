from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Product

admin.site.register(Product)




def edit_button(self, obj):
    url = reverse(
        "admin:products_product_change",
        args=[obj.id]
    )

    return format_html(
        '<a href="{}" '
        'style="background:#2563eb; color:white; '
        'padding:6px 12px; border-radius:5px; '
        'text-decoration:none;">Edit</a>',
        url
    )

edit_button.short_description = "Action"