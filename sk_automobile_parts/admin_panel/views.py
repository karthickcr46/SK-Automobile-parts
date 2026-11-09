from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from orders.models import Order, DeliveryPartner
from products.models import Product
from customers.models import Customer


@staff_member_required
def dashboard(request):
    context = {
        "product_count": Product.objects.count(),
        "order_count": Order.objects.count(),
        "customer_count": Customer.objects.count(),
        "partner_count": DeliveryPartner.objects.count(),

        "pending_orders": Order.objects.filter(
            order_status="PENDING"
        ).count(),

        "out_for_delivery": Order.objects.filter(
            order_status="OUT_FOR_DELIVERY"
        ).count(),

        "delivered_orders": Order.objects.filter(
            order_status="DELIVERED"
        ).count(),
    }

    return render(
        request,
        "admin_panel/dashboard.html",
        context
    )


@staff_member_required
def admin_orders(request):

    orders = Order.objects.select_related(
        "customer",
        "delivery_partner"
    ).order_by("-created_at")

    partners = DeliveryPartner.objects.filter(
        is_available=True
    )

    return render(
        request,
        "admin_panel/orders.html",
        {
            "orders": orders,
            "partners": partners,
        }
    )


@staff_member_required
def update_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        partner_id = request.POST.get(
            "delivery_partner"
        )

        status = request.POST.get(
            "order_status"
        )

        if partner_id:
            order.delivery_partner = get_object_or_404(
                DeliveryPartner,
                id=partner_id
            )
        else:
            order.delivery_partner = None

        if status:
            order.order_status = status

        order.save()

    return redirect("admin_orders")

@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related(
            "customer",
            "delivery_partner"
        ).prefetch_related(
            "items__product"
        ),
        id=order_id
    )

    return render(
        request,
        "admin_panel/order_detail.html",
        {
            "order": order
        }
    )