from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.delivery_login,
        name="delivery_login"
    ),

    path(
        "dashboard/",
        views.delivery_dashboard,
        name="delivery_dashboard"
    ),

    path(
        "logout/",
        views.delivery_logout,
        name="delivery_logout"
    ),

]