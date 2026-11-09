from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField()

    bike_model = models.CharField(max_length=100 ,default="All Bikes")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

