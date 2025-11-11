from django.shortcuts import render,redirect
from cart.models import CartItem
from django.contrib import messages
from .models import Order,OrderItem

def create_order(request):

    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('cart')

    total = 0
    if request.method =="post":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        
        total = sum(item.product.discounted_price() * item.quantity for item in cart_items)

        order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                total_price=total
            )
        
        for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.discounted_price()
                )

        cart_items.delete()
        return redirect('payment:process', order_id=order.id)
    else:
       
       for item in cart_items:
            total += item.product.discounted_price() * item.quantity

    
    total = round(total,2)
    context = {
          "total":total,
          "grand_total":total+150,
          'cart_items':cart_items,
    }

    return render(request, 'orders/checkout.html',context)