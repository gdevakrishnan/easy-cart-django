from django.shortcuts import render, redirect
from easy_cart_app.form import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

def home (request):
    return render(request, 'shop/index.html')

def register (request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST) # we send the data for validation
        if (form.is_valid()):
            form.save()
            messages.success(request, "Registeration successfull!!")
            return redirect("/login")
    return render(request, 'shop/register.html', {"form": form})

def login_page (request):
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
    category = Category.objects.filter(status = 0)
    return render(request, 'shop/collections.html', {"category": category})

def collections_view (request, name):
    if (Category.objects.filter(name = name, status = 0)):
        products = Product.objects.filter(category__name = name)
        return render(request, 'shop/products/index.html', { "products": products, "category": name })
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')

def product_view (request, cname, pname):
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
    return render(request, 'shop/features.html')