from django.db import models
from shop.models import Product
from accounts.models import User
from django.utils import timezone


class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="cart_user")
    product = models.ForeignKey(Product,related_name="cart_products",on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def sub_total(self):
        return self.product.discounted_price() * self.quantity
    
    def __str__(self):
        return str(self.product)

class Coupon(models.Model):
    CODE_TYPE_CHOICES = [
        ('fixed', 'Fixed Amount'),
        ('percent', 'Percentage'),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=CODE_TYPE_CHOICES, default='fixed')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to and self.active == True

    def __str__(self):
        return self.code
    


class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_wishlist")
    product = models.ForeignKey(Product,related_name="products_wishlist",on_delete=models.CASCADE)
