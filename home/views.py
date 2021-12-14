"""import "render" to render templates,all other for database connectivity"""
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authorization.views import login
from django.http import JsonResponse
from productorder.models import Order,Customer, OrderItem

from main.models import *

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user = request.user
        email = request.user.email
        name = str(request.user)
        create_customer = Customer.objects.get_or_create(user=user, email=email, name=name)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']

    context = all_categories()
    context['cartItems'] = cartItems

    return render(request, 'home.html', context)

def all_categories():
    men, women, kids = get_categories()
    men_category = conjoint_main_sub_categories(men)
    women_cateogry = conjoint_main_sub_categories(women)
    kids_category = conjoint_main_sub_categories(kids)

    context = {'men_category' : men_category,
               'women_category' : women_cateogry,
               'kids_category' : kids_category}

    return(context)

def conjoint_main_sub_categories(category):
    conjointed_category = {}
    for i in category:
        subcategory = SubCategory.objects.filter(category=i)
        for j in subcategory:
            if i not in conjointed_category:
                conjointed_category[i] = [j]
            else:
                conjointed_category[i].append(j)
    
    return(conjointed_category)

def get_categories():
    category_men = []
    category_women = []
    category_kids = []
    sex = Sex.objects.all()
    for i in sex:
        if str(i) == "male":
            category_m = Category.objects.filter(sex=i)
            category_men += category_m
        elif str(i) == "female":
            category_f = Category.objects.filter(sex=i)
            category_women += category_f
        elif str(i) == "kids":
            category_k = Category.objects.filter(sex=i)
            category_kids += category_k
    
    return(category_men, category_women, category_kids)

def show_products(request, pk):
    products = Product.objects.filter(category=pk)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items    
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']

    context = all_categories()
    context['cartItems'] = cartItems
    
    return render(request, 'products.html', context)


def product_details(request, product_name):
    product = Product.objects.get(name=product_name)
    context = all_categories()
    context['product'] = product
    return render(request, 'product_details.html', context)

def search(request):
    men_category, women_category, kids_catogry = all_categories()
    if request.method == "GET":
        searched = request.GET['search']
        search_capitalize = searched.capitalize()
        product = Product.objects.filter(name__contains=search_capitalize)

        context = all_categories()
        context['product'] = product

        return render(request, 'search.html', context)
    # else:
    #     return render(request, 'search.html')
