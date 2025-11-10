from django.db import models
from shop.models import Product
from accounts.models import User
class cart(models.Model):
    cart_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="cart_user")
    cart = models.ForeignKey(cart,related_name="cart_item",on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name="cart_products",on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)

    def sub_total(Self):
        return Self.product.discounted_price * Self.quantity
    
    def __str__(self):
        return str(self.product)
