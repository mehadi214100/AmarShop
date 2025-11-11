from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from decimal import Decimal
from django.utils import timezone
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True,max_length=150)
    image = models.ImageField(upload_to="category/",blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    is_popular = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_percentage = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(100)])
    stock  = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)
    unit = models.CharField(blank=True,max_length=50)
    rating = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])
    specification = RichTextField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def discounted_price(self):
        now = timezone.now()
        flash_sale = self.flash_sales.filter(
            is_active=True,
            start_time__lte=now,
            end_time__gte=now
        ).first()

        if flash_sale:
            discount = Decimal(1) - Decimal(flash_sale.discount_percentage) / Decimal(100)
            return round(self.price * discount,2)
        
        if self.discount_percentage:
            discount = Decimal(1) - Decimal(self.discount_percentage) / Decimal(100)
            return round(self.price * discount,2)
        return round(self.price,2)

    def get_ratings(self):
        return round(self.rating/5,2)


    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="products/")
    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
    def __str__(self):
            return f"Image for {self.product.name}"
    
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_reviews")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_reviews")
    rating = models.FloatField(blank=True,null=True,validators=[MinValueValidator(0), MaxValueValidator(5)])
    review = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} on {self.product.name}"
    

class FlashSale(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product,related_name="flash_sales")
    discount_percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

    def is_live(self):
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time