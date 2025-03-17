
from django.shortcuts import render, redirect


# Create your views here.


def home(request):
    return render(request,'home.html')

def mainPage(request):
    products = [
        {"name": "Paracetamol", "description": "Pain relief", "price": 5, 'img':'pill.jpeg'},
        {"name": "Vitamin C", "description": "Immune booster", "price": 10, 'img':'pill2.jpeg'},
        {"name": "Syrup", "description": "Cold", "price": 15, 'img':'syrup.jpeg'},
    ]
    return render(request, 'mainPage.html', {"products": products})