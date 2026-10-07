from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from products.models import Product, Category
from shops.models import Shop, ShopProduct
from orders.models import Order, Notification, Delivery


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')

        return render(
            request,
            'dashboard/admin_login.html',
            {
                'error': 'Invalid admin credentials'
            }
        )

    return render(
        request,
        'dashboard/admin_login.html'
    )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard_home(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    from payments.models import Payment

    product_count = Product.objects.count()
    shop_count = Shop.objects.count()
    order_count = Order.objects.count()

    customer_count = User.objects.filter(
        is_staff=False
    ).count()

    payment_count = Payment.objects.count()

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'product_count': product_count,
            'shop_count': shop_count,
            'order_count': order_count,
            'customer_count': customer_count,
            'payment_count': payment_count,
        }
    )


# =========================================================
# PRODUCTS
# =========================================================

def product_list(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    products = Product.objects.all()

    return render(
        request,
        'dashboard/products.html',
        {
            'products': products,
        }
    )


def product_add(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    categories = Category.objects.all()

    if request.method == 'POST':

        category_id = request.POST.get('category')
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        part_number = request.POST.get('part_number')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        compatibility = request.POST.get('compatibility')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')

        category = get_object_or_404(
            Category,
            id=category_id
        )

        Product.objects.create(
            category=category,
            name=name,
            brand=brand,
            part_number=part_number,
            description=description,
            price=price,
            stock=stock,
            image=image,
            compatibility=compatibility,
            is_active=is_active,
        )

        return redirect('admin_products')

    return render(
        request,
        'dashboard/product_add.html',
        {
            'categories': categories,
        }
    )


def product_edit(request, product_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    categories = Category.objects.all()

    if request.method == 'POST':

        product.category_id = request.POST.get('category')
        product.name = request.POST.get('name')
        product.brand = request.POST.get('brand')
        product.part_number = request.POST.get('part_number')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.compatibility = request.POST.get('compatibility')

        product.is_active = (
            request.POST.get('is_active') == 'on'
        )

        image = request.FILES.get('image')

        if image:
            product.image = image

        product.save()

        return redirect('admin_products')

    return render(
        request,
        'dashboard/product_edit.html',
        {
            'product': product,
            'categories': categories,
        }
    )


def product_delete(request, product_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':
        product.delete()
        return redirect('admin_products')

    return render(
        request,
        'dashboard/product_delete.html',
        {
            'product': product,
        }
    )


# =========================================================
# CATEGORIES
# =========================================================

def category_list(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            Category.objects.create(
                name=name,
                description=description
            )

            return redirect('admin_categories')

    categories = Category.objects.all()

    return render(
        request,
        'dashboard/categories.html',
        {
            'categories': categories,
        }
    )


def category_edit(request, category_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            category.name = name
            category.description = description
            category.save()

            return redirect('admin_categories')

    return render(
        request,
        'dashboard/category_edit.html',
        {
            'category': category,
        }
    )


def category_delete(request, category_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == 'POST':
        category.delete()
        return redirect('admin_categories')

    return render(
        request,
        'dashboard/category_delete.html',
        {
            'category': category,
        }
    )


# =========================================================
# SHOPS
# =========================================================

def shop_list(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    shops = Shop.objects.all().order_by('-created_at')

    return render(
        request,
        'dashboard/shops.html',
        {
            'shops': shops,
        }
    )


def shop_add(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':

        name = request.POST.get('name')
        owner_id = request.POST.get('owner')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        is_open = request.POST.get('is_open') == 'on'
        accepts_orders = request.POST.get('accepts_orders') == 'on'

        owner = get_object_or_404(
            User,
            id=owner_id
        )

        Shop.objects.create(
            owner=owner,
            name=name,
            phone=phone,
            address=address,
            city=city,
            latitude=latitude,
            longitude=longitude,
            is_open=is_open,
            accepts_orders=accepts_orders,
        )

        return redirect('admin_shops')

    users = User.objects.filter(
        is_staff=True
    ).order_by('username')

    return render(
        request,
        'dashboard/shop_add.html',
        {
            'users': users,
        }
    )


def shop_edit(request, shop_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    shop = get_object_or_404(
        Shop,
        id=shop_id
    )

    users = User.objects.filter(
        is_staff=True
    ).order_by('username')

    if request.method == 'POST':

        shop.name = request.POST.get('name')
        shop.owner_id = request.POST.get('owner')
        shop.phone = request.POST.get('phone')
        shop.address = request.POST.get('address')
        shop.city = request.POST.get('city')
        shop.latitude = request.POST.get('latitude')
        shop.longitude = request.POST.get('longitude')

        shop.is_open = request.POST.get('is_open') == 'on'
        shop.accepts_orders = request.POST.get('accepts_orders') == 'on'

        shop.save()

        return redirect('admin_shops')

    return render(
        request,
        'dashboard/shop_edit.html',
        {
            'shop': shop,
            'users': users,
        }
    )


def shop_delete(request, shop_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    shop = get_object_or_404(
        Shop,
        id=shop_id
    )

    if request.method == 'POST':
        shop.delete()
        return redirect('admin_shops')

    return render(
        request,
        'dashboard/shop_delete.html',
        {
            'shop': shop,
        }
    )


# =========================================================
# SHOP INVENTORY
# =========================================================

def inventory_list(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    inventory = ShopProduct.objects.select_related(
        'shop',
        'product'
    ).order_by('-updated_at')

    return render(
        request,
        'dashboard/inventory.html',
        {
            'inventory': inventory,
        }
    )


def inventory_add(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    shops = Shop.objects.all().order_by('name')

    products = Product.objects.filter(
        is_active=True
    ).order_by('name')

    if request.method == 'POST':

        shop_id = request.POST.get('shop')
        product_id = request.POST.get('product')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        is_available = request.POST.get('is_available') == 'on'

        shop = get_object_or_404(
            Shop,
            id=shop_id
        )

        product = get_object_or_404(
            Product,
            id=product_id,
            is_active=True
        )

        ShopProduct.objects.update_or_create(
            shop=shop,
            product=product,
            defaults={
                'price': price,
                'stock': stock,
                'is_available': is_available,
            }
        )

        return redirect('admin_inventory')

    return render(
        request,
        'dashboard/inventory_add.html',
        {
            'shops': shops,
            'products': products,
        }
    )


# =========================================================
# ORDERS
# =========================================================

def order_list(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    orders = Order.objects.select_related(
        'customer'
    ).prefetch_related(
        'items__product',
        'payment'
    ).order_by('-created_at')

    return render(
        request,
        'dashboard/orders.html',
        {
            'orders': orders,
        }
    )


def order_detail(request, order_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    order = get_object_or_404(
        Order.objects.select_related(
            'customer',
            'payment'
        ).prefetch_related(
            'items__product'
        ),
        id=order_id
    )

    # Delivery record, if it already exists
    delivery = Delivery.objects.filter(
        order=order
    ).select_related(
        'delivery_person'
    ).first()

    # Users whose profile role is delivery
    delivery_persons = User.objects.filter(
        is_active=True,
        profile__role='delivery'
    ).select_related(
        'profile'
    ).order_by('username')

    if request.method == 'POST':

        action = request.POST.get('action')

        # =================================================
        # ASSIGN DELIVERY PERSON
        # =================================================

        if action == 'assign_delivery':

            delivery_person_id = request.POST.get(
                'delivery_person'
            )

            if not delivery_person_id:

                messages.error(
                    request,
                    'Please select a delivery person.'
                )

                return redirect(
                    'admin_order_detail',
                    order_id=order.id
                )

            delivery_person = get_object_or_404(
                User.objects.filter(
                    is_active=True,
                    profile__role='delivery'
                ),
                id=delivery_person_id
            )

            delivery, created = Delivery.objects.get_or_create(
                order=order,
                defaults={
                    'delivery_person': delivery_person,
                    'status': (
                        'out_for_delivery'
                        if order.status == 'out_for_delivery'
                        else 'assigned'
                    )
                }
            )

            if not created:

                delivery.delivery_person = delivery_person

                if order.status == 'out_for_delivery':
                    delivery.status = 'out_for_delivery'

                elif delivery.status == 'delivered':
                    delivery.status = 'delivered'

                else:
                    delivery.status = 'assigned'

                delivery.save(
                    update_fields=[
                        'delivery_person',
                        'status',
                        'updated_at'
                    ]
                )

            messages.success(
                request,
                f'Delivery person "{delivery_person.username}" '
                f'has been assigned to order {order.order_number}.'
            )

            return redirect(
                'admin_order_detail',
                order_id=order.id
            )

        # =================================================
        # UPDATE ORDER STATUS
        # =================================================

        new_status = request.POST.get('status')

        valid_statuses = [
            'pending',
            'confirmed',
            'preparing',
            'out_for_delivery',
            'delivered',
            'cancelled',
        ]

        if new_status not in valid_statuses:

            messages.error(
                request,
                'Invalid order status.'
            )

            return redirect(
                'admin_order_detail',
                order_id=order.id
            )

        previous_status = order.status

        # -------------------------------------------------
        # UPDATE ORDER STATUS
        # -------------------------------------------------

        order.status = new_status

        order.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

        # =================================================
        # DELIVERY TRACKING
        # =================================================

        if new_status == 'out_for_delivery':

            delivery, created = Delivery.objects.get_or_create(
                order=order,
                defaults={
                    'status': 'out_for_delivery'
                }
            )

            if not created:

                delivery.status = 'out_for_delivery'

                delivery.save(
                    update_fields=[
                        'status',
                        'updated_at'
                    ]
                )

        # =================================================
        # DELIVERY COMPLETION
        # =================================================

        elif new_status == 'delivered':

            delivery = Delivery.objects.filter(
                order=order
            ).first()

            if delivery:

                delivery.status = 'delivered'
                delivery.delivered_at = timezone.now()

                delivery.save(
                    update_fields=[
                        'status',
                        'delivered_at',
                        'updated_at'
                    ]
                )

        # =================================================
        # CANCELLED ORDER
        # =================================================

        elif new_status == 'cancelled':

            delivery = Delivery.objects.filter(
                order=order
            ).first()

            if delivery:

                delivery.status = 'assigned'

                delivery.save(
                    update_fields=[
                        'status',
                        'updated_at'
                    ]
                )

        # =================================================
        # CUSTOMER NOTIFICATION + EMAIL
        # =================================================

        if previous_status != new_status:

            notification_data = {

                'confirmed': {
                    'title': 'Order Confirmed',
                    'message': (
                        f'Your order {order.order_number} '
                        'has been confirmed. '
                        'We will start preparing your order soon.'
                    ),
                },

                'preparing': {
                    'title': 'Your Order Is Being Prepared',
                    'message': (
                        f'Your order {order.order_number} '
                        'is now being prepared. '
                        'We are getting your items ready.'
                    ),
                },

                'out_for_delivery': {
                    'title': 'Your Order Is Out for Delivery',
                    'message': (
                        f'Your order {order.order_number} '
                        'is out for delivery. '
                        'Our delivery partner is on the way.'
                    ),
                },

                'delivered': {
                    'title': 'Order Delivered',
                    'message': (
                        f'Your order {order.order_number} '
                        'has been delivered successfully. '
                        'Thank you for shopping with '
                        'SK Automobile Parts!'
                    ),
                },

                'cancelled': {
                    'title': 'Order Cancelled',
                    'message': (
                        f'Your order {order.order_number} '
                        'has been cancelled.'
                    ),
                },

            }

            notification_info = notification_data.get(
                new_status
            )

            if notification_info:

                # -----------------------------------------
                # CREATE IN-APP NOTIFICATION
                # -----------------------------------------

                Notification.objects.create(
                    customer=order.customer,
                    order=order,
                    notification_type=new_status,
                    title=notification_info['title'],
                    message=notification_info['message'],
                )

                # -----------------------------------------
                # SEND EMAIL
                # -----------------------------------------

                if order.customer.email:

                    send_mail(
                        subject=notification_info['title'],
                        message=notification_info['message'],
                        from_email=None,
                        recipient_list=[
                            order.customer.email
                        ],

                        # IMPORTANT:
                        # Do not allow SMTP failure to break
                        # the order-status operation.
                        fail_silently=True,
                    )

        # =================================================
        # ADMIN SUCCESS MESSAGE
        # =================================================

        if new_status == 'out_for_delivery':

            messages.success(
                request,
                'Order is now out for delivery. '
                'Delivery tracking has been activated.'
            )

        else:

            messages.success(
                request,
                'Order status updated successfully.'
            )

        return redirect(
            'admin_order_detail',
            order_id=order.id
        )

    # Refresh delivery object before rendering
    delivery = Delivery.objects.filter(
        order=order
    ).select_related(
        'delivery_person'
    ).first()

    return render(
        request,
        'dashboard/order_detail.html',
        {
            'order': order,
            'delivery': delivery,
            'delivery_persons': delivery_persons,
        }
    )


# =========================================================
# CUSTOMERS
# =========================================================

def customer_list(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    customers = User.objects.filter(
        is_staff=False
    ).order_by('-date_joined')

    return render(
        request,
        'dashboard/customers.html',
        {
            'customers': customers,
        }
    )


# =========================================================
# PAYMENTS
# =========================================================

def payment_list(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')

    from payments.models import Payment

    payments = Payment.objects.select_related(
        'order',
        'customer'
    ).order_by('-created_at')

    return render(
        request,
        'dashboard/payments.html',
        {
            'payments': payments
        }
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

def admin_logout(request):

    logout(request)

    return redirect('admin_login')