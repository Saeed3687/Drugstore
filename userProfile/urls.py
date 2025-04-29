
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    
    path('profile/', views.profile, name='profile'),
    path('profile/user_info', views.userInfo, name='user_info'),
    path('profile/user_orders', views.userOrders, name='user_orders'),
  
    path('profile/user_info/update-user-info', views.update_user_info, name='update_user_info'),
    
]