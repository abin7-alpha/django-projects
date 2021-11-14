"""import "render" to render templates,all other for database connectivity"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authorization.views import login

from home.models import Men_Product, Men_category, Men_product_category
from home.models import Women_Product, Women_category, Women_product_category
from home.models import Kid_Product, Kid_category, Kid_product_category

# Create your views here.

def get_categories(gender_wise):
    """To create a dictionary of id(main category) as a key and name as a value, the initial stage 
    be like this [{'id' : 1, 'name' : 'topwear'}] after conversion {1 : 'topwear, 2 : 'bottomwear'}"""
    categories = gender_wise.objects.values('id', 'name')

    category_dict = {}
    for category in categories:
        category_dict[category['id']] = category['name']

    return category_dict

def get_sub_categories(gender_wise_product):
    """To create a dictionary that have key as id(category) 
    that matches to the id of subcategories(Top wear(id:1)- shirts(id:1),tshirts(id:1),etc..)
    and value with a list of subcategories that id matches i.e {1 : [formal_shirts,t-shirts,casual shirts]} so on"""
    sub_categories = gender_wise_product.objects.values('name', 'category_id')
    id_name_kind = gender_wise_product.objects.values_list('id', 'name')

    sorteds = {}
    count = 0
    for category in sub_categories:
        if category['category_id'] not in sorteds:
            sorteds[category['category_id']] = [id_name_kind[count]]
        else:
            sorteds[category['category_id']] += [id_name_kind[count]]
        count += 1

    return sorteds

def final_sorted_categories(category, product_category):
    categories = get_categories(category)
    sub_categories = get_sub_categories(product_category)

    for i,j in categories.items():
        if i in sub_categories.keys():
            sub_categories[j] = sub_categories.pop(i)

    return sub_categories

def home(request):
    # if not request.user.is_authenticated:
    #     request.user = None
    #     return redirect('home2')
    men_final_category = final_sorted_categories(Men_category, Men_product_category)
    women_final_category = final_sorted_categories(Women_category, Women_product_category)
    kid_final_category = final_sorted_categories(Kid_category, Kid_product_category)

    return render(request, 'home.html', 
                {'men_category' : men_final_category, 
                'women_category' : women_final_category,
                'kid_category': kid_final_category})

def home2(request):
    men_final_category = final_sorted_categories(Men_category, Men_product_category)
    women_final_category = final_sorted_categories(Women_category, Women_product_category)
    kid_final_category = final_sorted_categories(Kid_category, Kid_product_category)

    return render(request, 'home.html', 
                {'men_category' : men_final_category, 
                'women_category' : women_final_category,
                'kid_category': kid_final_category})


def show_products(pk, gender_product):
    products = gender_product.objects.all()
    sorted_products_details = {}
    for product in products:
        if product.category_id not in sorted_products_details:
            sorted_products_details[product.category_id] = [product]
        else:
            sorted_products_details[product.category_id].append(product)

    goods = None
    for product_id,product_details in sorted_products_details.items():
        if product_id == int(pk):
            goods = product_details

    context = {
        'products' : goods
    }

    return context

def details(gender_product, product_name):
    goods = None
    products = gender_product.objects.values("name", "price", "image", "description")
    for product in products:
        if product_name == product["name"]:
            goods = product

    return goods

def category():
    men_final_category = final_sorted_categories(Men_category, Men_product_category)
    women_final_category = final_sorted_categories(Women_category, Women_product_category)
    kid_final_category = final_sorted_categories(Kid_category, Kid_product_category)
    context = {
            'men_category' : men_final_category, 
            'women_category' : women_final_category,
            'kid_category': kid_final_category
            }
    
    return context

def show_products_men(request, pk):
    goods = show_products(pk, Men_Product)
    context = category()
    context['products'] = goods['products']

    return render(request, 'products.html', context)

def show_products_women(request, pk):
    goods = show_products(pk, Women_Product)
    context = category()
    context['products'] = goods['products']

    return render(request, 'products.html', context)

def show_products_kids(request, pk):
    goods = show_products(pk, Kid_Product)
    context = category()
    context['products'] = goods['products']

    return render(request, 'products.html', context)

def product_details(request, product_name):
    products_gender = [Men_Product, Women_Product, Kid_Product]
    goods = None
    for products in products_gender:
        if details(products, product_name):
            goods = details(products, product_name)
    context = category()
    context['product'] = goods
    
    return render(request, 'product_details.html', context)

def search(request):
    if request.method == "GET":
        searched = request.GET['search']
        search_capitalize = searched.capitalize()
        men_product = Men_Product.objects.filter(name__contains=search_capitalize)
        women_product = Women_Product.objects.filter(name__contains=searched)
        kid_product = Kid_Product.objects.filter(name__contains=searched)
        products = [men_product, women_product, kid_product]

        product_wanted = []
        for product in products:
            if product:
                product_wanted += product


        context = category()
        context['products'] = product_wanted

        return render(request, 'search.html', context)
    # else:
    #     return render(request, 'search.html')

