from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem,Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html', {'products': Product.objects.all()})

def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = Product.objects.get(id=id)
    order, _ = Order.objects.get_or_create(user=request.user, completed=False)
    item, _ = OrderItem.objects.get_or_create(order=order, product=product)
    item.quantity += 1
    item.save()
    return redirect('cart')

def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    order, _ = Order.objects.get_or_create(user=request.user, completed=False)
    items = OrderItem.objects.filter(order=order)

    total = 0
    for item in items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already exists'})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            login(request, user)  # 🔥 auto login after register
            return redirect('/')  # go to home

        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

from django.shortcuts import render, redirect
from .models import Order, OrderItem

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    order = Order.objects.get(user=request.user, completed=False)
    items = OrderItem.objects.filter(order=order)

    total = sum([item.product.price * item.quantity for item in items])

    if request.method == "POST":
        payment_method = request.POST.get('payment')

        # Save order as completed
        order.completed = True
        order.save()

        return render(request, 'success.html', {
            'method': payment_method
        })

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })


