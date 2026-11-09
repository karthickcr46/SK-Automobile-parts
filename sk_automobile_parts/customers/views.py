from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from products.models import Product
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect





def customer_details(request):

    # Customer is already logged in
    if request.session.get("customer_id"):
        return redirect("home")

    if request.method == "POST":

        phone = request.POST.get("phone", "").strip()

        customer = Customer.objects.filter(
            phone=phone
        ).first()

        if customer:

            request.session["customer_id"] = customer.id

            return redirect("home")

        request.session["new_customer_phone"] = phone

        return redirect("customer_register")

    return render(
        request,
        "customers/customer_details.html"
    )

def customer_register(request):

    # Get the new phone number
    phone = request.session.get("new_customer_phone")

    if not phone:
        return redirect("customer_details")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        pincode = request.POST.get("pincode", "").strip()

        # Make sure required details are entered
        if not name or not email or not address:
            return render(
                request,
                "customers/customer_register.html",
                # {
                #     "phone": phone,
                #     "error": "Please fill all required details."
                # }
            )

        # Create new customer
        customer = Customer.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )

        # Save customer ID
        request.session["customer_id"] = customer.id

        # Remove temporary phone
        request.session.pop("new_customer_phone", None)

        # Go to home
        return redirect("home")

    return render(
        request,
        "customers/customer_register.html",
        {
            "phone": phone
        }
    )





def my_details(request):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("customer_details")

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    return render(
        request,
        "customers/my_details.html",
        {
            "customer": customer
        }
    )






def home(request):

    products = Product.objects.all()[:8]

    bike_models = Product.objects.values_list(
        "bike_model",
        flat=True
    ).distinct()

    return render(
        request,
        "home.html",
        {
            "products": products,
            "bike_models": bike_models
        }
    )


def logout_customer(request):

    request.session.flush()

    return redirect("customer_details")


def customer_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "customers/login.html",
            {"error": "Invalid username or password."}
        )