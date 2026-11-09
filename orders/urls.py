from django.urls import path

from . import views


urlpatterns = [

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'detail/<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),

    path(
        'track/<int:order_id>/',
        views.track_order,
        name='track_order'
    ),

    # Delivery location update API
    path(
        'delivery/location/<int:order_id>/',
        views.update_delivery_location,
        name='update_delivery_location'
    ),

    path(
        'notifications/',
        views.notifications,
        name='notifications'
    ),

    path(
        'notifications/read/<int:notification_id>/',
        views.mark_notification_read,
        name='mark_notification_read'
    ),
]