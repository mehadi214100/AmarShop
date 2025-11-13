from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Product
from .models import Coupon,CartItem,Wishlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def viewcart(request):
    currenet_user = request.user
    cart_items = []
    total_price = 0

    if currenet_user.is_authenticated:
        cart_items = CartItem.objects.all().filter(user = currenet_user)
    
    for item in cart_items:
        total_price += item.product.discounted_price() * item.quantity
    
    coupon_id = request.session.get('coupon_id')
    discount = 0
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid():
                applied_coupon = coupon
                
                if applied_coupon.discount_type == 'fixed':
                    discount = applied_coupon.discount_value
                elif applied_coupon.discount_type == 'percent':
                    discount = total_price * (applied_coupon.discount_value / 100)
            else:
                request.session.pop('coupon_id', None)
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)
            
        request.session.pop('coupon_id', None)

    grand_total = total_price - discount if total_price > discount else 0

    context = {
        'total_price':total_price,
        'cart_items':cart_items,
        'discount':discount,
        'grand_total':grand_total,
    }

    return render(request,"cart/cart.html",context)

@login_required
def add_cart(request,product_id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(product=product,user=current_user)

    if cart_item.exists():
        cart_item = cart_item.first()
        cart_item.quantity +=1
        cart_item.save()
    else:
        CartItem.objects.create(product=product,user = current_user,quantity=1)
    
    messages.success(request, f'"{product.name}" added to cart successfully!')

    return redirect('product_details',product_name=product.slug)

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  
    return redirect('cart')


def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code').strip()
        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
            return redirect('cart')

        if not coupon.is_valid():
            messages.error(request, 'This coupon is expired or inactive.')
            return redirect('cart')

        
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        cart_total = sum(item.sub_total for item in cart_items)

        if cart_total < coupon.min_amount:
            messages.warning(request, f'Minimum cart total for this coupon is ${coupon.min_amount}.')
            return redirect('cart')

        
        request.session['coupon_id'] = coupon.id
        messages.success(request, f'Coupon "{coupon.code}" applied successfully!')
        return redirect('cart')
    else:
        return redirect('cart')

def remove_cart(request,item_id):
    user = request.user
    item =  get_object_or_404(CartItem, user=user, id=item_id)
    item.delete()
    return redirect('cart')


def addwishlist(request,item_id):
    user = request.user
    cart_item  = get_object_or_404(CartItem, user=user, id=item_id)
    product = cart_item.product
    cart_item ,created = Wishlist.objects.get_or_create(user=user,product=product)

    if created:
        messages.success(request, f"{product.name} added to your wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")

    return redirect('cart')


