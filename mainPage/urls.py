from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainPage, name = 'mainPage'),
    path('rate/<int:product_id>/',  views.submit_rating, name='submit_rating'),
    path('category/<str:category_name>/', views.category_view, name='category'),
]

