from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import userProfile, User
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Wishlist
from order.models import Order

@login_required
def profile(request):
    user_profile = userProfile.objects.filter(user=request.user).first()
    if not user_profile:
        return render(request, '404.html', status=404)

    orders = Order.objects.filter(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)
    total_order_amount = sum(order.total_price for order in orders)
    
    context = {
        "userProfile": user_profile,
        "totalOrder": orders.count(),
        'total_order_amount': total_order_amount,
        'totalwishlist': wishlist.count(),
        'orders': orders,
    }
    return render(request, 'profile/main.html', context)


@login_required
def myorders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    if not orders.exists():
        return render(request, '404.html', status=404)

    context = {'orders': orders}
    return render(request, 'profile/myorders.html', context)


@login_required
def settings(request):
    profile, created = userProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('settings')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profile/settings.html', context)


@login_required
def viewWishlist(request):
    products = Wishlist.objects.filter(user=request.user)
    if not products.exists():
        return render(request, '404.html', status=404)
    
    return render(request, 'profile/wishlist.html', {'products': products})


@login_required
def removeWishlist(request, item_id):
    product = Wishlist.objects.filter(user=request.user, id=item_id).first()
    if not product:
        return render(request, '404.html', status=404)

    product.delete()
    messages.success(request, "Wish item removed successfully")
    return redirect("viewWishlist")
