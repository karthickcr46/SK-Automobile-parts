from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
    entry_view,
    login_view,
    register_view,
    logout_view,
)


urlpatterns = [

    # Home
    path('', entry_view, name='home'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Custom Admin Dashboard
    path('admin-login/', include('dashboard.urls')),

    # Products
    path('products/', include('products.urls')),

    # Cart
    path('cart/', include('cart.urls')),

    # Orders
    path('orders/', include('orders.urls')),

    # Payments
    path('payments/', include('payments.urls')),
    path('delivery/', include('delivery.urls')),

    # Customer Authentication
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )