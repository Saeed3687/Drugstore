from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def profile(request):
    return render(request, 'user_profile.html')

@login_required
def userInfo(request):
    return render(request,"user_info.html")

@login_required
def userOrders(request):
    return render(request,"user_orders.html")

@login_required
def update_user_info(request):
    if request.method == "POST":
        new_email = request.POST.get('email')
        new_username = request.POST.get('username')

        user = request.user
        user.email = new_email
        user.first_name = new_username
        user.username = new_email  # If you want email as username

        if not new_email or not new_username:
            return render(request, 'user_info.html', {
                'error': 'All fields are required',
                'user': request.user
            })
        if User.objects.filter(username=new_email).exists():
            return render(request, 'user_info.html', {'error': 'Email already exists'})
        user.save()



    return redirect('user_profile')