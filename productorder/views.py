from django.shortcuts import render
from django.contrib.auth.models import User
from home.views import get_categories
from productorder.models import *
from django.http import JsonResponse
import json
import datetime

# Create your views here.

def cart(request):
    context = user_info(request)
    return render(request, 'cart.html', context)

def checkout(request):
    context = user_info(request)
    return render(request, 'checkout.html', context)

def user_info(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}

    context = {'items':items,'order': order, 'cartItems' : cartItems}

    return context

def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
 
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("item was added", safe=False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            zipcode = data['shipping']['zipcode'],
            state = data['shipping']['state'],
        )
    else:
        print("user is not authenticated..")
    print("data :",request.body)
    return JsonResponse('payment complete', safe=False)

def user_orders(request):
    total_orders = Order.objects.filter(customer = request.user.customer)
    completed_orders = []
    
    for orders in total_orders:
        if orders.complete == True:
            completed_orders.append(orders)

    products = {}
    for order in completed_orders:
        products[order] = order.orderitem_set.all()

    context = {'productss' : products}
    return render(request, 'orders.html', context)
