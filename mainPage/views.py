
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product

# Create your views here.


def home(request):
    return render(request,'home.html')

def mainPage(request):
    products = Product.objects.all()
    return render(request, 'mainPage.html', {"products": products})



def submit_rating(request, product_id):
    if request.method == "POST":
        new_rating = int(request.POST.get("rating", 0))
        product = get_object_or_404(Product, id=product_id)
        
        if 1 <= new_rating <= 5:
            product.update_rating(new_rating)
            return JsonResponse({"success": True, "new_rating": product.rating, "num_ratings": product.num_ratings})
        
    return JsonResponse({"success": False, "message": "Invalid rating"})
