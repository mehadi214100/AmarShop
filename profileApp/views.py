from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import userProfile,User
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Wishlist
from order.models import Order

def profile(request):

    user = userProfile.objects.filter(user=request.user).first
    orders = Order.objects.filter(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)
    totalOrder = orders.count()
    totalwishlist = wishlist.count()
    total_order_amount = 0

    if orders:
        for order in orders:
            total_order_amount += order.total_price

    context = {
        "userProfile":user,
        "totalOrder":totalOrder,
        'total_order_amount':total_order_amount,
        'totalwishlist':totalwishlist,
        'orders':orders,
    }

    return render(request,'profile/main.html',context)


def myorders(request):

    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
         'orders':orders,
    }

    return render(request,'profile/myorders.html',context)

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


def viewWishlist(request):
    products = Wishlist.objects.filter(user = request.user)
    return render(request,'profile/wishlist.html',{'products':products})

def removeWishlist(request,item_id):
    products = Wishlist.objects.filter(user = request.user,id=item_id)
    products.delete()
    messages.success(request,"Wish item Remove Success")
    return redirect("viewWishlist")