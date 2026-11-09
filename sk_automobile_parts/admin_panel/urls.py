from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.dashboard,
        name="admin_dashboard"
    ),

    path(
        "orders/",
        views.admin_orders,
        name="admin_orders"
    ),

    path(
        "orders/<int:order_id>/update/",
        views.update_order,
        name="update_order"
    ),

    path(
        "orders/<int:order_id>/",
        views.order_detail,
        name="admin_order_detail"
    ),
]