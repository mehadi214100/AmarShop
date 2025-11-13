from cart.models import CartItem

def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    return {'cart_item_count': count}
