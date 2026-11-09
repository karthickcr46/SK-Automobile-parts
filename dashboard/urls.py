from django.urls import path

from . import views


urlpatterns = [

    # Admin login
    path(
        '',
        views.admin_login,
        name='admin_login'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard_home,
        name='dashboard_home'
    ),

    # Products
    path(
        'products/',
        views.product_list,
        name='admin_products'
    ),

    path(
        'products/add/',
        views.product_add,
        name='product_add'
    ),

    path(
        'products/edit/<int:product_id>/',
        views.product_edit,
        name='product_edit'
    ),

    path(
        'products/delete/<int:product_id>/',
        views.product_delete,
        name='product_delete'
    ),

    # Categories
    path(
        'categories/',
        views.category_list,
        name='admin_categories'
    ),

    path(
        'categories/edit/<int:category_id>/',
        views.category_edit,
        name='category_edit'
    ),

    path(
        'categories/delete/<int:category_id>/',
        views.category_delete,
        name='category_delete'
    ),

    # Shops
    path(
        'shops/',
        views.shop_list,
        name='admin_shops'
    ),

    path(
        'shops/add/',
        views.shop_add,
        name='shop_add'
    ),

    path(
        'shops/edit/<int:shop_id>/',
        views.shop_edit,
        name='shop_edit'
    ),

    path(
        'shops/delete/<int:shop_id>/',
        views.shop_delete,
        name='shop_delete'
    ),

    # Inventory
    path(
        'inventory/',
        views.inventory_list,
        name='admin_inventory'
    ),

    path(
        'inventory/add/',
        views.inventory_add,
        name='inventory_add'
    ),

    # Orders
    path(
        'orders/',
        views.order_list,
        name='admin_orders'
    ),
    # Customers
    path(
        'customers/',
         views.customer_list,
         name='admin_customers'
    ),
    path(
        'payments/',
        views.payment_list, 
        name='admin_payments'
    ),

    path(
        'orders/<int:order_id>/',
        views.order_detail,
        name='admin_order_detail'
    ),

    # Logout
    path(
        'logout/',
        views.admin_logout,
        name='admin_logout'
    ),
]