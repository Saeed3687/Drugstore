from django.shortcuts import render, get_object_or_404,redirect
from mainPage.models import Product, Comment
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def productPage(request, id):
    product = get_object_or_404(Product, id=id)
    comments = product.comments.all()
    return render(request, 'product-page.html', {'product': product, 'comments': comments})
@login_required
def rate_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        new_rating = int(request.POST.get("rating", 0))
       
             
        if 1 <= new_rating <= 5:
            product.update_rating(new_rating)
            print(new_rating)
            return redirect('productPage',id=id)
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

@user_passes_test(lambda u: u.is_superuser)
def admin_reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        reply = request.POST.get('reply', '').strip()
        comment.reply = reply
        comment.save()
        messages.success(request, 'Reply saved!')
    return redirect('productPage', id=comment.product.id)    
    