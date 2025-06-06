from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart, CartItem
from mainPage.models import Product
from django.contrib import messages
from userProfile.models import UserProfile, Order, OrderItem

# Create your views here.

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    return render(request, 'My-Cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is available
    if not product.available or product.count <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock!")
        return redirect('productPage', id=product_id)
    
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price': product.price}
    )
    
    if not item_created:
        # Check if adding one more would exceed available count
        if cart_item.quantity + 1 > product.count:
            messages.error(request, f"Sorry, only {product.count} items of {product.name} are available!")
            return redirect('view_cart')
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to cart successfully!")
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart successfully!")
    return redirect('view_cart')

@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if requested quantity is available
        if quantity > cart_item.product.count:
            return JsonResponse({
                'success': False,
                'message': f"Sorry, only {cart_item.product.count} items are available!"
            })
            
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({
                'success': True,
                'new_total': str(cart_item.get_cost())
            })
    return JsonResponse({'success': False})

@login_required
def proceed_to_checkout(request):
    cart = get_object_or_404(Cart, user=request.user, is_paid=False)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Save shipping information
        fullName = request.POST.get('fullName')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        zipCode = request.POST.get('zipCode', '')
        
        # Update user profile with the latest information
        request.user.first_name = fullName
        request.user.save()
        
        profile.address = address
        profile.phone_number = phone
        profile.save()
        
        # Redirect to payment page
        return redirect('payment')
        
    return render(request, 'proceed-checkout.html', {
        'cart': cart,
        'profile': profile,
        'user': request.user
    })

@login_required
def payment(request):
    cart = get_object_or_404(Cart, user=request.user, is_paid=False)
    if request.method == 'POST':
        # Check if all items are still available
        for cart_item in cart.items.all():
            if not cart_item.product.available or cart_item.quantity > cart_item.product.count:
                messages.error(request, f"Sorry, {cart_item.product.name} is no longer available in the requested quantity!")
                return redirect('view_cart')
        
        # Here you would integrate with your payment gateway
        # For now, we'll just mark the cart as paid and create an order
        profile = UserProfile.objects.get(user=request.user)
        
        # Create order with tracking code
        order = Order.objects.create(
            user=request.user,
            tracking_code=Order.generate_tracking_code(),
            total_amount=cart.get_total_price(),
            shipping_address=profile.address,
            phone_number=profile.phone_number
        )
        
        # Create order items and update product counts
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                quantity=cart_item.quantity,
                price=cart_item.price
            )
            # Decrease product count
            cart_item.product.decrease_count(cart_item.quantity)
        
        # Mark cart as paid
        cart.is_paid = True
        cart.save()
        
        messages.success(request, f"Payment successful! Your tracking code is {order.tracking_code}")
        return redirect('user_orders')
    return render(request, 'pay.html', {'cart': cart})
