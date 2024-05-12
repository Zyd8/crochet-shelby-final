from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . models import Product, Order, Cart, CartItem, MyUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


def home(request):
    audio_products = Product.objects.filter(category='Audio')
    home_products = Product.objects.filter(category='Home')
    accessories_products = Product.objects.filter(category='Accessories')

    return render(request, 'home.html', {
        'audio_products': audio_products,
        'home_products': home_products,
        'accessories_products': accessories_products
    })

def room(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'room.html', {'product': product})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return redirect('signin')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'signin.html')


from .models import MyUser  


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password or not confirm_password:
            messages.error(request, 'Please fill out all fields.')
            return redirect('signup')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('signup')

        # Check if the username is already taken
        if MyUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('signup')

        user = MyUser.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home') 

    return render(request, 'signup.html')


def signout(request):
    logout(request)
    return redirect('home')


from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price',  'category', 'image1', 'image2', 'image3', 'description']

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})


from django.db.models import Sum
from django.db.models import Sum, F, ExpressionWrapper, FloatField


def room(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        additional_notes = request.POST.get('additional_notes')
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.create(order=cart, product=product, quantity=quantity, additional_notes=additional_notes)
        cart.shipping_fee = 50

        total_price = cart.cartitem_set.aggregate(
            total_price=ExpressionWrapper(
                Sum(F('quantity') * F('product__price')),
                output_field=FloatField()
            )
        )['total_price']
        total_price += cart.shipping_fee
        cart.total_price = total_price if total_price is not None else 0
        
        cart.save()
        
        return redirect('room', product_id=product_id)
    
    return render(request, 'room.html', {'product': product})


def cart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        gcash_number = request.POST.get('gcash_number')
        shipping_address = request.POST.get('address')
        
        cart = Cart.objects.get(id=cart_id)
        cart.save()
        
        order = Order.objects.create(cart=cart, contact_number=gcash_number, shipping_address=shipping_address)
        
        return redirect('payment.html')
        
    else:
        cart_items = CartItem.objects.filter(order__user=request.user)
        
        if not cart_items:
            has_cart = False
        else:
            has_cart = True
            for item in cart_items:
                item.total = item.product.price * item.quantity
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        return render(request, 'cart.html', {'cart_items': cart_items, 'cart': cart, 'has_cart': has_cart})
    
def payment(request):
    return render(request, 'payment.html')

 