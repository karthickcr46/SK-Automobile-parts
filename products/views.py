from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product


def home(request):
    return render(request, 'products/home.html')


def product_list(request):
    products = Product.objects.filter(is_active=True)

    return render(
        request,
        'products/product_list.html',
        {
            'products': products,
        }
    )


def shop(request):
    products = Product.objects.filter(is_active=True)

    # -------------------------
    # Search
    # -------------------------
    search_query = request.GET.get('q', '').strip()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(brand__icontains=search_query)
            | Q(part_number__icontains=search_query)
            | Q(compatibility__icontains=search_query)
            | Q(category__name__icontains=search_query)
        )

    # -------------------------
    # Category filter
    # -------------------------
    category_name = request.GET.get('category', '').strip()

    if category_name:
        products = products.filter(
            category__name__iexact=category_name
        )

    # -------------------------
    # Stock filter
    # -------------------------
    in_stock = request.GET.get('in_stock')

    if in_stock == '1':
        products = products.filter(stock__gt=0)

    # -------------------------
    # Sorting
    # -------------------------
    sort = request.GET.get('sort', 'popular')

    if sort == 'price_low':
        products = products.order_by('price')

    elif sort == 'price_high':
        products = products.order_by('-price')

    elif sort == 'newest':
        products = products.order_by('-created_at')

    else:
        # Popular / default
        products = products.order_by('-id')

    return render(
        request,
        'products/shop.html',
        {
            'products': products,
            'search_query': search_query,
            'category_name': category_name,
            'in_stock': in_stock,
            'sort': sort,
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product
        }
    )