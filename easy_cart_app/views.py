from django.shortcuts import render
from .models import *

def home (request):
    return render(request, 'shop/index.html')

def register (request):
    return render(request, 'shop/register.html')

def collections (request):
    category = Category.objects.filter(status = 0)
    return render(request, 'shop/collections.html', {"category": category})

def features (request):
    return render(request, 'shop/features.html')