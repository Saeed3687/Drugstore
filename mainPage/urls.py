from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainPage, name = 'mainPage'),
    path('rate/<int:product_id>/',  views.submit_rating, name='submit_rating'),
]
