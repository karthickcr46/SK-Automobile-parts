from django.db import models
from django.contrib.auth.models import User
from orders.models import Order


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('card', 'Credit / Debit Card'),
        ('net_banking', 'Net Banking'),
        ('cod', 'Cash on Delivery'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.order.order_number} - {self.payment_method}"