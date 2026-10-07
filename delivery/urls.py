from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.delivery_dashboard,
        name='delivery_dashboard'
    ),
]