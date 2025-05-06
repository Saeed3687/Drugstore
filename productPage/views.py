from django.shortcuts import render, get_object_or_404,redirect
from mainPage.models import Product

def productPage(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product-page.html', {'product': product})

def rate_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        new_rating = int(request.POST.get("rating", 0))
        # match new_rating:
        #     case 1:
        #         new_rating = 5
        #     case 2:
        #         new_rating = 4
        #     case 4:
        #         new_rating = 2
        #     case 5:
        #         new_rating = 1
       
             
        if 1 <= new_rating <= 5:
            product.update_rating(new_rating)
            print(new_rating)
            return redirect('productPage',id=id)
    return render(request, 'product-page.html', {'product': product})    
    