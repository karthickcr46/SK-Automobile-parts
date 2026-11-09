from django.urls import path
from . import views


urlpatterns = [

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Payment
    path(
        "payment/",
        views.payment_page,
        name="payment_page"
    ),

    # Order success
    path(
        "success/<int:order_id>/",
        views.order_success,
        name="order_success"
    ),

    # Customer orders
    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    # Customer tracking page
    path(
        "track/<int:order_id>/",
        views.track_order,
        name="track_order"
    ),

    # Customer gets delivery partner GPS
    path(
        "track/<int:order_id>/location/",
        views.delivery_location_api,
        name="delivery_location_api"
    ),

    # Delivery partner GPS page
    path(
        "delivery/<int:order_id>/",
        views.delivery_tracking,
        name="delivery_tracking"
    ),

    # Delivery partner sends GPS
    path(
        "delivery/<int:order_id>/location/",
        views.update_delivery_location,
        name="update_delivery_location"
    ),
]