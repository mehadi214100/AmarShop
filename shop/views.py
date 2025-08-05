from django.shortcuts import render
from .models import Product,Category
def home(request):
    categories = Category.objects.all().filter(is_available=True)
    popular_categories = Category.objects.filter(is_available=True,is_popular=True)[:3]
    products = Product.objects.select_related('category').filter(available=True,category__is_available=True)
    context = {
        "categories":categories,
        "popular_categories":popular_categories,
        "products":products,
    }
    return render(request,"shop/home.html",context)


def all_products(request,category=None):
    if category:
        products = Product.objects.select_related('category').filter(available=True,category__is_available=True,category__slug=category)
    else:
        products = Product.objects.select_related('category').filter(available=True,category__is_available=True)

    context = {
        "products":products,
    }
    return render(request,"shop/product_list.html",context)


def product_details(request,product_name):
    product = Product.objects.get(slug = product_name)
    cat = product.category
   
    related_products = Product.objects.all().filter(category =  cat)
   
    context = {
        "product":product,
        "related_products":related_products,
    }
    return render(request,"shop/product_details.html",context)