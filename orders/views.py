from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string

from cart.models import Cart
from .models import Order, OrderItem, Notification, Delivery


@login_required
def checkout(request):

    cart = Cart.objects.filter(
        customer=request.user
    ).first()

    if not cart or not cart.items.exists():
        return redirect('cart_view')

    if request.method == 'POST':

        shipping_address = request.POST.get(
            'shipping_address',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        if not shipping_address or not phone:
            return render(
                request,
                'orders/checkout.html',
                {
                    'cart': cart,
                    'error': (
                        'Please enter your delivery '
                        'address and phone number.'
                    )
                }
            )

        # Check stock before creating the order.
        for cart_item in cart.items.select_related('product'):

            if cart_item.quantity > cart_item.product.stock:
                return render(
                    request,
                    'orders/checkout.html',
                    {
                        'cart': cart,
                        'error': (
                            f'Sorry, only '
                            f'{cart_item.product.stock} units of '
                            f'{cart_item.product.name} are available.'
                        )
                    }
                )

        # Create the order safely as one database operation.
        with transaction.atomic():

            order_number = (
                'SK'
                + get_random_string(
                    length=10,
                    allowed_chars='0123456789'
                )
            )

            total_amount = cart.total_price()

            order = Order.objects.create(
                customer=request.user,
                order_number=order_number,
                total_amount=total_amount,
                shipping_address=shipping_address,
                phone=phone,
                status='pending'
            )

            # Create order items.
            for cart_item in cart.items.select_related('product'):

                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

        # Send customer to payment page.
        return redirect(
            'payment_page',
            order_id=order.id
        )

    return render(
        request,
        'orders/checkout.html',
        {
            'cart': cart
        }
    )


@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    return render(
        request,
        'orders/order_success.html',
        {
            'order': order
        }
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )


# =========================================================
# CUSTOMER LIVE ORDER TRACKING
# =========================================================

@login_required
def track_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    # -----------------------------------------------------
    # CUSTOMER LIVE LOCATION API
    # -----------------------------------------------------
    #
    # The customer tracking page calls:
    #
    # /orders/track/<order_id>/?location=1
    #
    # This returns the latest GPS coordinates saved
    # by the delivery person's browser.
    # -----------------------------------------------------

    if request.GET.get('location') == '1':

        delivery = getattr(
            order,
            'delivery',
            None
        )

        # Delivery record does not exist yet.
        if not delivery:

            return JsonResponse({
                'success': True,
                'available': False,
                'status': order.status,
                'message': (
                    'Delivery has not been assigned yet.'
                )
            })

        # Delivery is not currently out for delivery.
        if delivery.status != 'out_for_delivery':

            return JsonResponse({
                'success': True,
                'available': False,
                'status': delivery.status,
                'message': (
                    'Live tracking is not active.'
                )
            })

        # Delivery is out for delivery but GPS has
        # not sent a location yet.
        if (
            delivery.current_latitude is None
            or delivery.current_longitude is None
        ):

            return JsonResponse({
                'success': True,
                'available': False,
                'status': delivery.status,
                'message': (
                    'Waiting for delivery GPS location.'
                )
            })

        # Return the latest real GPS coordinates.
        return JsonResponse({

            'success': True,

            'available': True,

            'status': delivery.status,

            'latitude': float(
                delivery.current_latitude
            ),

            'longitude': float(
                delivery.current_longitude
            ),

            'updated_at': (
                delivery.updated_at.isoformat()
            )
        })

    # Normal customer tracking page.
    return render(
        request,
        'orders/track_order.html',
        {
            'order': order
        }
    )


# =========================================================
# DELIVERY LOCATION UPDATE API
# =========================================================

@login_required
def update_delivery_location(request, order_id):

    # Only delivery users can update delivery locations.
    if not hasattr(request.user, 'profile'):

        return JsonResponse(
            {
                'success': False,
                'message': 'Delivery profile not found.'
            },
            status=403
        )

    if request.user.profile.role != 'delivery':

        return JsonResponse(
            {
                'success': False,
                'message': 'Only delivery personnel can update location.'
            },
            status=403
        )

    # Only allow POST requests.
    if request.method != 'POST':

        return JsonResponse(
            {
                'success': False,
                'message': 'Only POST requests are allowed.'
            },
            status=405
        )

    # Get the delivery record.
    delivery = get_object_or_404(
        Delivery,
        order_id=order_id,
        delivery_person=request.user
    )

    # Location should only be updated while delivering.
    if delivery.status != 'out_for_delivery':

        return JsonResponse(
            {
                'success': False,
                'message': (
                    'Location updates are allowed only '
                    'while the order is out for delivery.'
                )
            },
            status=400
        )

    # Read latitude and longitude.
    latitude = request.POST.get(
        'latitude'
    )

    longitude = request.POST.get(
        'longitude'
    )

    # Make sure both values were received.
    if not latitude or not longitude:

        return JsonResponse(
            {
                'success': False,
                'message': (
                    'Latitude and longitude are required.'
                )
            },
            status=400
        )

    # Validate and convert coordinates.
    try:

        latitude = float(latitude)

        longitude = float(longitude)

    except (TypeError, ValueError):

        return JsonResponse(
            {
                'success': False,
                'message': (
                    'Latitude and longitude must be valid numbers.'
                )
            },
            status=400
        )

    # Validate geographic ranges.
    if not -90 <= latitude <= 90:

        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid latitude.'
            },
            status=400
        )

    if not -180 <= longitude <= 180:

        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid longitude.'
            },
            status=400
        )

    # Save the latest delivery location.
    delivery.current_latitude = latitude

    delivery.current_longitude = longitude

    delivery.save(
        update_fields=[
            'current_latitude',
            'current_longitude',
            'updated_at'
        ]
    )

    return JsonResponse(
        {
            'success': True,

            'message': 'Delivery location updated successfully.',

            'latitude': float(
                delivery.current_latitude
            ),

            'longitude': float(
                delivery.current_longitude
            ),

            'updated_at': (
                delivery.updated_at.isoformat()
            ),
        }
    )


# =========================================================
# CUSTOMER NOTIFICATIONS
# =========================================================

@login_required
def notifications(request):

    user_notifications = Notification.objects.filter(
        customer=request.user
    ).select_related(
        'order'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'orders/notifications.html',
        {
            'notifications': user_notifications
        }
    )


@login_required
def mark_notification_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        customer=request.user
    )

    notification.is_read = True

    notification.save(
        update_fields=['is_read']
    )

    return redirect(
        'notifications'
    )