from django.urls import path
from . import views  # Import your views
# from mainPage import views as user_profile  # Import your views

urlpatterns = [
    
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/user_info', views.userInfo, name='user_info'),
    path('profile/user_orders', views.userOrders, name='user_orders'),
  
    path('profile/user_info/update-user-info', views.update_user_info, name='update_user_info'),
    path('order/<str:tracking_code>/', views.order_details, name='order_details'),
]