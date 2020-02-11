from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'home.html')

def product_page(request):
    return render(request,'product-page.html')

def cart(request):
    return render(request,'cart.html')

def profile(request):
    return render(request,'profile.html')