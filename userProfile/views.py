from django.shortcuts import render

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