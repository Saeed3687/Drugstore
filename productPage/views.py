from django.shortcuts import render, get_object_or_404,redirect
from mainPage.models import Product, Comment
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def productPage(request, id):
    product = get_object_or_404(Product, id=id)
    comments = product.comments.all()
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = product.user_ratings.get(user=request.user).rating
        except:
            pass
    return render(request, 'product-page.html', {
        'product': product, 
        'comments': comments,
        'user': request.user,
        'user_rating': user_rating
    })
@login_required
def rate_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        new_rating = int(request.POST.get("rating", 0))
        
        if 1 <= new_rating <= 5:
            user_rating = product.update_rating(request.user, new_rating)
            messages.success(request, f"Your rating of {new_rating} stars has been saved!")
            return redirect('productPage', id=id)
        else:
            messages.error(request, "Invalid rating value. Please rate between 1 and 5 stars.")
    
    return render(request, 'product-page.html', {'product': product})    

@login_required
def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(
                product=product,
                user=request.user,
                text=text
            )
            messages.success(request, 'Your comment has been added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty!')
    return redirect('productPage', id=product_id)    

@superuser_required
def admin_reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        reply = request.POST.get('reply', '').strip()
        comment.reply = reply
        comment.save()
        messages.success(request, 'Reply saved!')
    return redirect('productPage', id=comment.product.id)    
    