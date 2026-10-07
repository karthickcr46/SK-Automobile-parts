from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import UserProfile


def entry_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            if request.user.profile.role == 'delivery':
                return redirect('delivery_dashboard')

        return redirect('/products/shop/')

    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            if request.user.profile.role == 'delivery':
                return redirect('delivery_dashboard')

        return redirect('/products/shop/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not email or not password:
            return render(
                request,
                'accounts/register.html',
                {'error': 'Please fill in all fields.'}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'accounts/register.html',
                {'error': 'Username already exists.'}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            role='customer'
        )

        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            if request.user.profile.role == 'delivery':
                return redirect('delivery_dashboard')

        return redirect('/products/shop/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            # Delivery user → Delivery Dashboard
            if hasattr(user, 'profile') and user.profile.role == 'delivery':
                return redirect('delivery_dashboard')

            # Normal customer → Customer Shop
            return redirect('/products/shop/')

        return render(
            request,
            'accounts/login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')