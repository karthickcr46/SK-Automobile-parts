from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from customers.models import Customer
from cart.models import Cart

from .models import (
    Order,
    OrderItem,
    DeliveryLocation,
)


# ==========================================================
# CHECKOUT
# ==========================================================

def checkout(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("customer_details")

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    cart = get_object_or_404(
        Cart,
        customer=customer
    )

    items = cart.items.all()

    if not items.exists():
        return redirect("cart")

    total = sum(
        item.total_price()
        for item in items
    )

    if request.method == "POST":

        payment_method = request.POST.get(
            "payment_method"
        )

        # Checkout sends only COD or ONLINE
        valid_methods = [
            "COD",
            "ONLINE",
        ]

        if payment_method not in valid_methods:

            return render(
                request,
                "orders/checkout.html",
                {
                    "customer": customer,
                    "items": items,
                    "total": total,
                    "error": "Please select a payment method.",
                }
            )

        # -------------------------------
        # CASH ON DELIVERY
        # -------------------------------

        if payment_method == "COD":

            return create_order(
                request,
                customer,
                cart,
                items,
                total,
                payment_method="COD",
                payment_status="PENDING"
            )

        # -------------------------------
        # ONLINE PAYMENT
        # -------------------------------

        request.session["payment_method"] = "ONLINE"
        request.session["payment_total"] = str(total)

        return redirect("payment_page")

    return render(
        request,
        "orders/checkout.html",
        {
            "customer": customer,
            "items": items,
            "total": total,
        }
    )


# ==========================================================
# PAYMENT PAGE
# ==========================================================

def payment_page(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("customer_details")

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    cart = get_object_or_404(
        Cart,
        customer=customer
    )

    items = cart.items.all()

    if not items.exists():
        return redirect("cart")

    total = sum(
        item.total_price()
        for item in items
    )

    payment_method = request.session.get(
        "payment_method"
    )

    if payment_method != "ONLINE":
        return redirect("checkout")

    valid_online_methods = [
        "UPI",
        "CARD",
        "NET_BANKING",
    ]

    # ======================================================
    # PAYMENT SUBMISSION
    # ======================================================

    if request.method == "POST":

        submitted_method = request.POST.get(
            "payment_method"
        )

        if submitted_method not in valid_online_methods:

            return render(
                request,
                "orders/payment.html",
                {
                    "customer": customer,
                    "total": total,
                    "payment_method": "ONLINE",
                    "error": "Please select a valid payment method.",
                }
            )

        # ==================================================
        # CHECK STOCK
        # ==================================================

        for item in items:

            if item.product.stock < item.quantity:

                return render(
                    request,
                    "orders/payment.html",
                    {
                        "customer": customer,
                        "total": total,
                        "payment_method": "ONLINE",
                        "error": (
                            f"Insufficient stock for "
                            f"{item.product.name}."
                        ),
                    }
                )

        # ==================================================
        # DEMO TRANSACTION ID
        # ==================================================

        transaction_id = get_random_string(
            length=16,
            allowed_chars=(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )
        )

        payment_status = "PAID"

        # ==================================================
        # CREATE ORDER
        # ==================================================

        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            address=customer.address,
            payment_method=submitted_method,
            payment_status=payment_status,
            payment_id=transaction_id,
            order_status="CONFIRMED",
        )

        # ==================================================
        # CREATE ORDER ITEMS
        # ==================================================

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # ==================================================
        # REDUCE STOCK
        # ==================================================

        for item in items:

            item.product.stock -= item.quantity
            item.product.save()

        # ==================================================
        # SEND EMAILS
        # ==================================================

        send_order_emails(
            order,
            customer
        )

        # ==================================================
        # CLEAR CART
        # ==================================================

        items.delete()

        # ==================================================
        # CLEAR PAYMENT SESSION
        # ==================================================

        request.session.pop(
            "payment_method",
            None
        )

        request.session.pop(
            "payment_total",
            None
        )

        # ==================================================
        # SUCCESS
        # ==================================================

        return redirect(
            "order_success",
            order_id=order.id
        )

    # ======================================================
    # DISPLAY PAYMENT PAGE
    # ======================================================

    return render(
        request,
        "orders/payment.html",
        {
            "customer": customer,
            "total": total,
            "payment_method": "ONLINE",
        }
    )


# ==========================================================
# CREATE COD ORDER
# ==========================================================

def create_order(
    request,
    customer,
    cart,
    items,
    total,
    payment_method,
    payment_status
):

    # ======================================================
    # CHECK STOCK
    # ======================================================

    for item in items:

        if item.product.stock < item.quantity:

            return render(
                request,
                "orders/checkout.html",
                {
                    "customer": customer,
                    "items": items,
                    "total": total,
                    "error": (
                        f"Insufficient stock for "
                        f"{item.product.name}."
                    ),
                }
            )

    # ======================================================
    # CREATE ORDER
    # ======================================================

    order = Order.objects.create(
        customer=customer,
        total_amount=total,
        address=customer.address,
        payment_method=payment_method,
        payment_status=payment_status,
        order_status="CONFIRMED",
    )

    # ======================================================
    # CREATE ORDER ITEMS
    # ======================================================

    for item in items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    # ======================================================
    # REDUCE STOCK
    # ======================================================

    for item in items:

        item.product.stock -= item.quantity
        item.product.save()

    # ======================================================
    # SEND EMAIL
    # ======================================================

    send_order_emails(
        order,
        customer
    )

    # ======================================================
    # CLEAR CART
    # ======================================================

    items.delete()

    # ======================================================
    # SUCCESS
    # ======================================================

    return redirect(
        "order_success",
        order_id=order.id
    )


# ==========================================================
# SEND ORDER EMAILS
# ==========================================================

def send_order_emails(order, customer):

    items_text = ""

    for item in order.items.all():

        items_text += (
            f"Product: {item.product.name}\n"
            f"Bike Model: {item.product.bike_model}\n"
            f"Quantity: {item.quantity}\n"
            f"Price: ₹{item.price}\n"
            f"Total: ₹{item.price * item.quantity}\n\n"
        )

    # ======================================================
    # CUSTOMER EMAIL
    # ======================================================

    customer_email_message = f"""
Hello {customer.name},

Thank you for ordering from SK Automobile Parts.

Your order has been successfully placed.

================================
ORDER DETAILS
================================

Order ID: #{order.id}

{items_text}

Total Amount: ₹{order.total_amount}

================================
PAYMENT DETAILS
================================

Payment Method:
{order.get_payment_method_display()}

Payment Status:
{order.payment_status}

Payment ID:
{order.payment_id or "N/A"}

================================
DELIVERY DETAILS
================================

Name: {customer.name}
Phone: {customer.phone}
Email: {customer.email}

Address:
{customer.address}

City: {customer.city}
State: {customer.state}
Pincode: {customer.pincode}

Order Status:
{order.get_order_status_display()}

Thank you for shopping with
SK Automobile Parts.
"""

    send_mail(
        subject=f"Order Confirmation - #{order.id}",
        message=customer_email_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            customer.email
        ],
        fail_silently=False,
    )

    # ======================================================
    # ADMIN EMAIL
    # ======================================================

    admin_email_message = f"""
NEW ORDER RECEIVED

==============================

Order ID: #{order.id}

================================
CUSTOMER DETAILS
================================

Name: {customer.name}
Phone: {customer.phone}
Email: {customer.email}

Address:
{customer.address}

City: {customer.city}
State: {customer.state}
Pincode: {customer.pincode}

================================
ORDER DETAILS
================================

{items_text}

Total Amount:
₹{order.total_amount}

================================
PAYMENT DETAILS
================================

Payment Method:
{order.get_payment_method_display()}

Payment Status:
{order.payment_status}

Payment ID:
{order.payment_id or "N/A"}

Order Status:
{order.get_order_status_display()}

================================

Please check the Django Admin panel
for complete order information.

SK Automobile Parts
"""

    send_mail(
        subject=f"New Order Received - #{order.id}",
        message=admin_email_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            settings.ADMIN_EMAIL
        ],
        fail_silently=False,
    )


# ==========================================================
# ORDER SUCCESS
# ==========================================================

def order_success(request, order_id):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("customer_details")

    order = get_object_or_404(
        Order,
        id=order_id,
        customer_id=customer_id
    )

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order
        }
    )


# ==========================================================
# MY ORDERS
# ==========================================================

def my_orders(request):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("customer_details")

    orders = (
        Order.objects
        .filter(customer_id=customer_id)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )


# ==========================================================
# CUSTOMER - TRACK ORDER
# ==========================================================

def track_order(request, order_id):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("customer_details")

    order = get_object_or_404(
        Order,
        id=order_id,
        customer_id=customer_id
    )

    return render(
        request,
        "orders/track_order.html",
        {
            "order": order
        }
    )


# ==========================================================
# CUSTOMER - GET DELIVERY LOCATION
# ==========================================================

def delivery_location_api(request, order_id):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:

        return JsonResponse(
            {
                "success": False,
                "error": "Not logged in"
            },
            status=401
        )

    order = get_object_or_404(
        Order,
        id=order_id,
        customer_id=customer_id
    )

    # Live location is available ONLY
    # when order is Out for Delivery.

    if order.order_status != "OUT_FOR_DELIVERY":

        return JsonResponse({
            "success": True,
            "available": False,
            "message": (
                "Live location will start when "
                "the order is Out for Delivery."
            )
        })

    try:

        location = order.delivery_location

    except DeliveryLocation.DoesNotExist:

        return JsonResponse({
            "success": True,
            "available": False
        })

    # Location has been disabled
    if not location.is_active:

        return JsonResponse({
            "success": True,
            "available": False
        })

    return JsonResponse({

        "success": True,

        "available": True,

        "latitude": location.latitude,

        "longitude": location.longitude,

        "accuracy": location.accuracy,

        "updated_at": location.updated_at.isoformat(),

        "is_active": location.is_active,

    })


# ==========================================================
# DELIVERY PARTNER - UPDATE GPS LOCATION
# ==========================================================

import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from .models import Order, DeliveryLocation


@require_POST
def update_delivery_location(request, order_id):

    partner_id = request.session.get(
        "delivery_partner_id"
    )

    if not partner_id:
        return JsonResponse(
            {
                "error": "Delivery partner not logged in"
            },
            status=401
        )


    order = get_object_or_404(
        Order,
        id=order_id
    )


    if order.delivery_partner_id != partner_id:

        return JsonResponse(
            {
                "error":
                "You are not assigned to this order"
            },
            status=403
        )


    if order.order_status != "OUT_FOR_DELIVERY":

        return JsonResponse(
            {
                "error":
                "Order is not out for delivery"
            },
            status=403
        )


    try:

        data = json.loads(
            request.body
        )

        latitude = float(
            data.get("latitude")
        )

        longitude = float(
            data.get("longitude")
        )

        accuracy = data.get("accuracy")

        if accuracy is not None:
            accuracy = float(accuracy)


    except (
        ValueError,
        TypeError,
        json.JSONDecodeError
    ):

        return JsonResponse(
            {
                "error":
                "Invalid location data"
            },
            status=400
        )


    location, created = DeliveryLocation.objects.update_or_create(

        order=order,

        defaults={
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy,
            "is_active": True,
        }

    )


    return JsonResponse(
        {
            "success": True,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "accuracy": location.accuracy,
        }
    )
# ==========================================================
# DELIVERY PARTNER - LIVE TRACKING PAGE
# ==========================================================

def delivery_tracking(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    # ======================================================
    # LIVE GPS ONLY AFTER OUT FOR DELIVERY
    # ======================================================

    if order.order_status != "OUT_FOR_DELIVERY":

        return redirect(
            "delivery_dashboard"
        )

    # ======================================================
    # DELIVERY PARTNER MUST BE ASSIGNED
    # ======================================================

    if not order.delivery_partner:

        return redirect(
            "delivery_dashboard"
        )

    return render(
        request,
        "orders/delivery_tracking.html",
        {
            "order": order
        }
    )