from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('products_men/<int:pk>/', views.show_products_men, name="products_men"),
    path('products_women/<int:pk>/', views.show_products_women, name="products_women"),
    path('products_kids/<int:pk>/', views.show_products_kids, name="products_kids"),
    path('product_details/<str:product_name>/', views.product_details, name="product_deatils")
]