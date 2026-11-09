from django.shortcuts import render, redirect, get_object_or_404

from customers.models import Customer
from products.models import Product

from .models import Cart, CartItem


def add_to_cart(request, product_id):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("customer_details")

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    product = get_object_or_404(
        Product,
        id=product_id
    )

    # Don't add if product is out of stock
    if product.stock <= 0:
        return redirect("products")

    # Get or create customer's cart
    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    # Get or create cart item
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    # Increase quantity if item already exists
    if not created:

        if item.quantity < product.stock:
            item.quantity += 1
            item.save()

    return redirect("cart")





def cart_view(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("customer_details")

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    # Get customer's cart
    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    # Get all cart items
    items = cart.items.all()

    # Calculate total
    total = sum(
        item.total_price()
        for item in items
    )

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "items": items,
            "total": total
        }
    )


def increase_quantity(request, item_id):

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

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    # Don't exceed available stock
    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect("cart")


def decrease_quantity(request, item_id):

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

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")


def remove_from_cart(request, item_id):

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

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    item.delete()

    return redirect("cart")