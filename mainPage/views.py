
from django.shortcuts import render, redirect,get_object_or_404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product, Category

# Create your views here.


def home(request):
    return render(request,'home.html')

def mainPage(request):

    categories = Category.objects.prefetch_related('products').all()  # Fetch categories with products
    products = Product.objects.all()  # Fetch all products

    return render(request, 'mainPage.html', {'categories': categories, 'products': products})


def submit_rating(request, product_id):
    if request.method == "POST":
        new_rating = int(request.POST.get("rating", 0))
        product = get_object_or_404(Product, id=product_id)
        
        if 1 <= new_rating <= 5:
            product.update_rating(new_rating)
            return JsonResponse({"success": True, "new_rating": product.rating, "num_ratings": product.num_ratings})
        
    return JsonResponse({"success": False, "message": "Invalid rating"})

# def category_view(request, category_name):
#     products = Product.objects.filter(category=category_name)  # Filter products by category
    
#     return render(request, 'category.html', {'products': products, 'category_name': category_name})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    return render(request, 'category.html', {'category': category, 'products': products})
