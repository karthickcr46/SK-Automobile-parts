from django.urls import path
from . import views

urlpatterns = [
    path("", views.customer_details, name="customer_details"),

    path(
        "customer-register/",
        views.customer_register,
        name="customer_register"
    ),
    path("home/", views.home, name="home"),
    path("my-details/", views.my_details, name="my_details"),
    path("logout/", views.logout_customer, name="logout_customer"),
]

