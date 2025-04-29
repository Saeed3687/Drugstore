
from django.shortcuts import render, redirect,get_object_or_404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

@login_required
def add_changes(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.get(email=email)
        user.first_name = name
        user.email = email
        # Check if user already exists
        if User.objects.filter(username=email).exists():
            return render(request, 'logPage.html', {'error': 'Email already exists'})
        user.save()
        return redirect('user_info')

    return render(request, 'logPage.html')
@login_required
def user_profile(request):
    return render(request, 'user_profile.html', {'user': request.user})

