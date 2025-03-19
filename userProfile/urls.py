
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    
    path('profile/', views.profile, name='profile'),
]