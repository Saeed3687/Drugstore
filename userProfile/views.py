from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Order
# Create your views here.


@login_required


def user_profile(request):
    
    profile, created = UserProfile.objects.get_or_create(user= request.user)
    print(profile.address)
    return render(request, 'user_profile.html', {'user': request.user, 'profile': profile})



@login_required

def userInfo(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'user_info.html', {
        'user': request.user,
        'profile': profile,
    })

@login_required
def userOrders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "user_orders.html", {'orders': orders})



@login_required
def update_user_info(request):
    user = request.user
   
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        new_email = request.POST.get('email')
        new_username = request.POST.get('username')
        new_address = request.POST.get('address')
        new_phone_number = request.POST.get('phone_number')

        # Validate input
        if not new_email or not new_username:
            return render(request, 'user_info.html', {
                'error': 'Email and username are required',
                'user': user,
                'profile': profile
            })

        # Check if email (username) already exists and belongs to a different user
        if User.objects.filter(username=new_email).exclude(id=user.id).exists():
            return render(request, 'user_info.html', {
                'error': 'Email already in use by another account',
                'user': user,
                'profile': profile
            })
        

        # Update User fields
        user.email = new_email
        user.username = new_email  # optional: if email is used as username
        user.first_name = new_username
        user.save()
        if new_address == None:
            new_address = ''
        if new_phone_number == None:
            new_phone_number = ''
        # Update UserProfile fields
        profile.address = new_address
        profile.phone_number = new_phone_number
        profile.save()

        return redirect('user_info')

    # Handle GET request fallback
    return render(request, 'user_info.html', {'user': user, 'profile': profile})

@login_required
def order_details(request, tracking_code):
    order = get_object_or_404(Order, tracking_code=tracking_code, user=request.user)
    return render(request, 'order_details.html', {
        'order': order,
        'user': request.user
    })
