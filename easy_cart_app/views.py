from django.http import JsonResponse
from django.shortcuts import render, redirect
from easy_cart_app.form import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import json

def home (request):
    return render(request, 'shop/index.html')

def register (request):
    if request.user.is_authenticated:
        return redirect('/')
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST) # we send the data for validation
        if (form.is_valid()):
            form.save()
            messages.success(request, "Registeration successfull!!")
            return redirect("/login")
    return render(request, 'shop/register.html', {"form": form})

def login_page (request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            messages.success(request, "Logged in successfully")
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "Invalid username or password")
            redirect('/login')
    return render(request, 'shop/login.html')

def logout_page (request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout Successfully")
    return redirect('/')

def collections (request):
    if not request.user.is_authenticated:
        return redirect('/login')
    category = Category.objects.filter(status = 0)
    return render(request, 'shop/collections.html', {"category": category})

def collections_view (request, name):
    if not request.user.is_authenticated:
        return redirect('/login')

    if (Category.objects.filter(name = name, status = 0)):
        products = Product.objects.filter(category__name = name)
        return render(request, 'shop/products/index.html', { "products": products, "category": name })
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')

def product_view (request, cname, pname):
    if not request.user.is_authenticated:
        return redirect('/login')
    if (Category.objects.filter(name = cname, status = 0)):
        if (Product.objects.filter(name = pname, status = 0)):
            product_details = Product.objects.filter(name = pname, status = 0).first()
            return render(request, 'shop/products/product.html', {"product": product_details, "pname": pname, "cname": cname})
        else:
            messages.warning(request, "No such product found")
            return redirect(f'collections/{cname}')
    else:
        messages.warning(request, "No such category found")
        return redirect(f'collections/{cname}')


def features (request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'shop/features.html')

def add_to_cart (request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']

            product = Product.objects.get(id=product_id)
            if product:
                if Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'message': 'Product already in cart'}, status = 200)
                else:
                    if product.quantity >= int(product_qty):
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'message': 'Product added to the cart'}, status = 200)
                    else:
                        return JsonResponse({'message': 'Product out of stock'}, status = 400)
        else:
            return JsonResponse({'message': 'Login to add cart'}, status = 400)
    else:
        return JsonResponse({'message': 'Invalid Access'}, status = 400)

def cart(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    products = Cart.objects.filter(user=request.user)
    total_amount = sum(item.total_cost for item in products)

    return render(request, 'shop/cart.html', {"products": products, "total_amount": total_amount})

def delete_cart_item(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    cartitem = Cart.objects.get(id=pid)
    if cartitem:
        cartitem.delete()
        messages.success(request, "Cart item not found")
        return redirect('/login')
    else:
        messages.warning(request, "Cart item not found")
        return redirect('/cart')