from django.shortcuts import render
from django.contrib.auth.models import User
from productorder.models import *
from django.http import JsonResponse
import json

# Create your views here.

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}

    context = {'items':items,'order': order, 'cartItems' : cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

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
    # if request.method == "POST":
    #     customer = request.user.customer
    #     order = Order.objects.get(customer=customer, complete=False)
    #     address = request.POST.get('address')
    #     city = request.POST.get('city')
    #     state = request.POST.get('state')
    #     zip_code = request.POST.get('zipcode')
    #     ShippingAddress.objects.create(customer=customer, order = order, address=address,
    #                                    city=city, state=state, zipcode=zip_code)
    print("data :",request.body)
    return JsonResponse('payment complete', safe=False)

        

