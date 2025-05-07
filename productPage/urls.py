
from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:id>/', views.productPage, name='productPage'),
    path('product/rate_product/<int:id>/', views.rate_product, name='rate_product'),
    

]
