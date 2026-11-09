from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order


def delivery_dashboard(request):
    """
    Show orders assigned to the delivery partner.

    For now, this uses the delivery_partner_id stored in the session.
    """

    partner_id = request.session.get("delivery_partner_id")

    if not partner_id:
        return render(
            request,
            "delivery/dashboard.html",
            {
                "orders": [],
                "error": "Delivery partner is not logged in."
            }
        )

    orders = Order.objects.filter(
        delivery_partner_id=partner_id
    ).select_related(
        "customer",
        "delivery_partner"
    ).order_by("-created_at")

    return render(
        request,
        "delivery/dashboard.html",
        {
            "orders": orders
        }
    )


from django.shortcuts import render, redirect
from orders.models import DeliveryPartner


def delivery_login(request):

    if request.method == "POST":

        phone = request.POST.get("phone", "").strip()

        partner = DeliveryPartner.objects.filter(
            phone=phone
        ).first()

        if partner:

            request.session["delivery_partner_id"] = partner.id

            return redirect("delivery_dashboard")

        return render(
            request,
            "delivery/login.html",
            {
                "error": "Delivery partner not found."
            }
        )

    return render(
        request,
        "delivery/login.html"
    )

def delivery_logout(request):

    request.session.pop(
        "delivery_partner_id",
        None
    )

    return redirect("delivery_login")