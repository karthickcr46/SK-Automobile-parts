from django.shortcuts import render
from .models import Product


def product_list(request):

    products = Product.objects.all()

    search = request.GET.get("search")
    bike_model = request.GET.get("bike_model")

    if search:
        products = products.filter(
            name__icontains=search
        )

    if bike_model:
        products = products.filter(
            bike_model__icontains=bike_model
        )

    bike_models = (
        Product.objects
        .values_list("bike_model", flat=True)
        .distinct()
    )

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "bike_models": bike_models,
            "search": search,
            "selected_bike": bike_model,
        }
    )


