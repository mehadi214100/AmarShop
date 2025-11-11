from django.shortcuts import render,redirect
from accounts.models import userProfile,User
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Wishlist


def profile(request):

    user = userProfile.objects.filter(user=request.user).first

    context = {
        "userProfile":user
    }

    return render(request,'profile/main.html',context)



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