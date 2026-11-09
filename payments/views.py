from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.crypto import get_random_string

from cart.models import Cart
from orders.models import Order
from .models import Payment


@login_required
def payment_page(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    existing_payment = Payment.objects.filter(
        order=order
    ).first()

    if existing_payment:
        return redirect(
            'order_success',
            order_id=order.id
        )

    if request.method == 'POST':

        payment_method = request.POST.get(
            'payment_method'
        )

        valid_methods = [
            'upi',
            'card',
            'net_banking',
            'cod'
        ]

        if payment_method not in valid_methods:

            return render(
                request,
                'payments/payment.html',
                {
                    'order': order,
                    'error': 'Please select a payment method.'
                }
            )

        # Get the customer's cart.
        cart = Cart.objects.filter(
            customer=request.user
        ).first()

        if not cart:
            return render(
                request,
                'payments/payment.html',
                {
                    'order': order,
                    'error': 'Your cart could not be found.'
                }
            )

        # Process payment, stock and cart together.
        with transaction.atomic():

            # Lock the products while updating stock.
            order_items = order.items.select_related(
                'product'
            )

            for order_item in order_items:

                product = order_item.product

                if order_item.quantity > product.stock:

                    return render(
                        request,
                        'payments/payment.html',
                        {
                            'order': order,
                            'error': (
                                f'Sorry, only '
                                f'{product.stock} units of '
                                f'{product.name} are available.'
                            )
                        }
                    )

            transaction_id = get_random_string(
                length=16,
                allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            )

            if payment_method == 'cod':
                payment_status = 'pending'
            else:
                payment_status = 'paid'

            # Create payment record.
            Payment.objects.create(
                order=order,
                customer=request.user,
                payment_method=payment_method,
                amount=order.total_amount,
                status=payment_status,
                transaction_id=transaction_id
            )

            # Reduce product stock.
            for order_item in order.items.select_related('product'):

                product = order_item.product

                product.stock -= order_item.quantity

                product.save(
                    update_fields=[
                        'stock',
                        'updated_at'
                    ]
                )

            # Confirm the order.
            order.status = 'confirmed'
            order.save(
                update_fields=[
                    'status',
                    'updated_at'
                ]
            )

            # Clear the customer's cart.
            cart.items.all().delete()

        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(
        request,
        'payments/payment.html',
        {
            'order': order
        }
    )