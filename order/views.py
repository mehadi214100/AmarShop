from django.shortcuts import render, redirect, get_object_or_404
from cart.models import CartItem
from django.contrib import messages
from .models import Order, OrderItem
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
import uuid
from django.contrib.auth import login

def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    total = sum(item.product.discounted_price() * item.quantity for item in cart_items)
    shipping = 150
    grand_total = total + shipping

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            postal_code=postal_code,
            total_price=grand_total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discounted_price()
            )

        cart_items.delete()
        return redirect(f'/order/payment-process/{order.id}/')

    return render(request, 'orders/checkout.html', {
        "total": total,
        "grand_total": grand_total,
        "cart_items": cart_items,
    })


def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    sslcz = SSLCOMMERZ({
        'store_id': settings.SSLCZ_STORE_ID,
        'store_pass': settings.SSLCZ_STORE_PASS,
        'issandbox': settings.SSLCZ_IS_SANDBOX,
    })

    post_body = {
        'total_amount': float(order.total_price),
        'currency': "BDT",
        'tran_id': f"ORDER_{order.id}_{uuid.uuid4().hex[:6]}",
        'success_url': request.build_absolute_uri('/order/payment-success/'),
        'fail_url': request.build_absolute_uri('/order/payment-fail/'),
        'cancel_url': request.build_absolute_uri('/order/payment-cancel/'),
        'emi_option': 0,
        'cus_name': order.full_name,
        'cus_email': order.email,
        'cus_phone': order.phone,
        'cus_add1': order.address,
        'cus_city': order.city,
        'cus_country': "Bangladesh",
        'shipping_method': "Courier",
        'num_of_item': order.items.count(),
        'product_name': "Cart Items",
        'product_category': "Mixed",
        'product_profile': "general",
        'ship_name': order.full_name,
        'ship_add1': order.address,     
        'ship_city': order.city,       
        'ship_country': "Bangladesh",
        'ship_postcode': order.postal_code,
    }

    response = sslcz.createSession(post_body)


    if response.get('GatewayPageURL'):
        order.transaction_id = post_body['tran_id']
        order.save()
        return HttpResponseRedirect(response['GatewayPageURL'])
    else:
        return render(request, 'payment/error.html', {'response': response})


@csrf_exempt
def payment_success(request):
    tran_id = request.POST.get('tran_id')
    val_id = request.POST.get('val_id')

    sslcz = SSLCOMMERZ({
        'store_id': settings.SSLCZ_STORE_ID,
        'store_pass': settings.SSLCZ_STORE_PASS,
        'issandbox': settings.SSLCZ_IS_SANDBOX,
    })

    post_data = request.POST.dict()

    if sslcz.hash_validate_ipn(post_data):
        response = sslcz.validationTransactionOrder(val_id)
        if response.get('status') == 'VALID':
            order = Order.objects.filter(transaction_id=tran_id).first()
            if order:
                order.status = 'Paid'
                order.paid = True
                order.save()
               
                user = order.user
                if user:
                    login(request, user)  # logs in the user automatically
            return render(request, 'payment/payment_success.html', {'order': order})
        else:
            return render(request, 'payment/payment_fail.html', {'msg': 'Invalid transaction'})
    else:
        return render(request, 'payment/payment_fail.html', {'msg': 'Hash validation failed'})


@csrf_exempt
def payment_fail(request):
    return render(request, 'payment/payment_fail.html', {'msg': 'Payment failed.'})


@csrf_exempt
def payment_cancel(request):
    return render(request, 'payment/payment_cancel.html', {'msg': 'Payment was cancelled.'})
