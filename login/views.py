
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.


def register_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if user already exists

        
        if User.objects.filter(username=email).exists():
            return render(request, 'logPage.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        return redirect('login')

    return render(request, 'logPage.html')

def login_view(request):

    if request.user.is_authenticated:
        return redirect('mainPage')  

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('mainPage') 
        else:
            return render(request, 'logPage.html', {'error': 'Invalid Email or Password'})

    return render(request, 'logPage.html')

