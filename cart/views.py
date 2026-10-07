from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .models import Cart, CartItem


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    if product.stock <= 0:
        return redirect('cart_view')

    cart, created = Cart.objects.get_or_create(
        customer=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:

        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart_view')


@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(
        customer=request.user
    )

    return render(
        request,
        'cart/cart.html',
        {
            'cart': cart
        }
    )


@login_required
def update_cart_quantity(request, item_id, action):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__customer=request.user
    )

    product = cart_item.product

    if action == 'increase':

        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()

    elif action == 'decrease':

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__customer=request.user
    )

    cart_item.delete()

    return redirect('cart_view')