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


def all_products(request):
    products = Product.objects.select_related('category').filter(available=True,category__is_available=True)
    context = {
        "products":products,
    }
    return render(request,"shop/product_list.html",context)