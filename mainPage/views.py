from django.shortcuts import render, redirect,get_object_or_404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product, Category, Comment
from Cart.models import Cart, CartItem
from userProfile.models import UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Avg, F
from django.http import HttpResponseForbidden




def home(request):
    return render(request,'home.html')
@never_cache
def mainPage(request):
    # Get the 5 most recent comments
    recent_comments = Comment.objects.all().order_by('-created_at')[:5]
    categories = Category.objects.prefetch_related('products').all()  # Fetch categories with products
    products = Product.objects.all()  # Fetch all products

    return render(request, 'mainPage.html', {'categories': categories, 'products': products, 'comments': recent_comments})


def submit_rating(request, product_id):
    if request.method == "POST":
        new_rating = int(request.POST.get("rating", 0))
        product = get_object_or_404(Product, id=product_id)
        
        if 1 <= new_rating <= 5:
            product.update_rating(new_rating)
            return JsonResponse({"success": True, "new_rating": product.rating, "num_ratings": product.num_ratings})
        
    return JsonResponse({"success": False, "message": "Invalid rating"})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    
    # Get sort parameter from request
    sort_by = request.GET.get('sort')
    if sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'available':
        products = products.order_by('-available', 'name')  # Available first, then by name

    # Pagination
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'category.html', {
        'category': category, 
        'products': page_obj,
        'sort': sort_by  # Pass the current sort to maintain it in pagination
    })


@login_required


def user_profile(request):
    
    profile, created = UserProfile.objects.get_or_create(user= request.user)
    print(profile.address)
    return render(request, 'user_profile.html', {'user': request.user, 'profile': profile})



# Search

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []

    return render(request, 'search.html', {'products': products, 'query': query})

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@superuser_required
def reports(request):
    # Get total sales by summing the price * quantity of all cart items in paid carts
    total_sales = CartItem.objects.filter(
        cart__is_paid=True
    ).aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    # Get best-selling products
    best_selling_products = Product.objects.annotate(
        total_sold=Sum('cartitem__quantity')
    ).order_by('-total_sold')[:5]

    # Get most popular products by rating
    most_popular_products = Product.objects.annotate(
        avg_rating=Avg('user_ratings__rating')
    ).order_by('-avg_rating')[:5]

    # Get sales by category
    sales_by_category = Product.objects.values('category__name').annotate(
        total_sales=Sum('cartitem__quantity')
    ).order_by('-total_sales')

    # Get recent orders with their totals
    recent_orders = Cart.objects.filter(is_paid=True).order_by('-created_at')[:10]
    orders_with_totals = []
    for order in recent_orders:
        total = sum(item.get_cost() for item in order.items.all())
        orders_with_totals.append({
            'order': order,
            'total': total
        })

    context = {
        'total_sales': total_sales,
        'best_selling_products': best_selling_products,
        'most_popular_products': most_popular_products,
        'sales_by_category': sales_by_category,
        'recent_orders': orders_with_totals,
    }
    
    return render(request, 'reports.html', context)

