from django.shortcuts import render

def home (request):
    return render(request, 'shop/index.html')

def register (request):
    return render(request, 'shop/register.html')

def features (request):
    return render(request, 'shop/features.html')