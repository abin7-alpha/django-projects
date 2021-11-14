from django.urls import path
from . import views
from authorization import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('home2', views.home2, name="home2"),
    path('products_men/<int:pk>/', views.show_products_men, name="products_men"),
    path('products_women/<int:pk>/', views.show_products_women, name="products_women"),
    path('products_kids/<int:pk>/', views.show_products_kids, name="products_kids"),
    path('product_details/<str:product_name>/', views.product_details, name="product_deatils"),
    path('search_category', views.search, name="search_category"),
]

urlpatterns_auth =[
    path('register/', auth_views.register, name="register"),
    path('register/login/', auth_views.login, name="login"),
    path('logout/', auth_views.logout, name="logout"),
]

urlpatterns += urlpatterns_auth