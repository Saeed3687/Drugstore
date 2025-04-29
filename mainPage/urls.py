from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainPage, name = 'mainPage'),
    path('rate/<int:product_id>/',  views.submit_rating, name='submit_rating'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('profile/', views.user_profile, name='user_profile'),
    path('search/', views.search, name='search'),

]

