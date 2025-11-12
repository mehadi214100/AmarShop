from django.shortcuts import render
from .models import Product,Category,FlashSale
from django.utils import timezone
from .models import CarouselBanner

def home(request):
    categories = Category.objects.all().filter(is_available=True)
    popular_categories = Category.objects.filter(is_available=True,is_popular=True)[:3]
    products = Product.objects.select_related('category').filter(available=True,category__is_available=True)
    
    
    now = timezone.now()
    flash_sales = FlashSale.objects.filter(is_active=True, end_time__gte=now).order_by('-start_time')

    sales_with_countdown = []

    for sale in flash_sales:
        remaining = sale.end_time - now
        if remaining.total_seconds() > 0:
            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
        else:
            days = hours = minutes = seconds = 0

        sales_with_countdown.append({
            'sale': sale,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
        })

    banners = CarouselBanner.objects.filter(is_active=True).order_by('order')
    
    context = {
        "categories":categories,
        "popular_categories":popular_categories,
        "products":products,
        "sales_with_countdown":sales_with_countdown,
        "banners": banners,
    }
    return render(request,"shop/home.html",context)


def all_products(request,category_wase=None):

    products = Product.objects.select_related('category').filter(
        available=True,
        category__is_available=True
    )

    if category_wase:
        products = Product.objects.select_related('category').filter(category__slug=category_wase)
    

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    sort_by = request.GET.get('sort_by')
    category = request.GET.get('category')

    if category:
        if category != "all":
            products = Product.objects.select_related('category').filter(category__slug=category)
    

    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)


    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')
    elif sort_by == 'new_arrivals':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')

    categories = Category.objects.all().filter(is_available=True)
       

    context = {
        "products":products,
        'categories':categories,
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


def search_product(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    
    context = {
        "products":products,
    }
    return render(request,"shop/product_list.html",context)


def flash_product(request,flash_id):
    sale = FlashSale.objects.all().filter(id=flash_id).first()
    context = {
        "sale":sale,
    }
    return render(request,"shop/flash_product.html",context)