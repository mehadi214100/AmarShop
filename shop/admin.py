from django.contrib import admin
from django.utils.text import slugify
from .models import Category, Product, ProductImage, Review, FlashSale

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_popular', 'created_at')
    prepopulated_fields = {"slug": ("name",)}  
    search_fields = ('name',)
    list_filter = ('created_at',)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discounted_price_display', 'slug', 'available', 'stock', 'rating')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('available', 'category', 'created_at')
    search_fields = ('name', 'category__name')
    inlines = [ProductImageInline, ReviewInline]

    def discounted_price_display(self, obj):
        return obj.discounted_price()
    discounted_price_display.short_description = 'Discounted Price'



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__name',)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    search_fields = ('user__email', 'product__name')
    list_filter = ('rating', 'created_at')


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'discount_percentage', 'is_active')
    list_filter = ('is_active', 'start_time', 'end_time')
    search_fields = ('name',)
    filter_horizontal = ('products',)



from .models import CarouselBanner

@admin.register(CarouselBanner)
class CarouselBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order", "created_at")
    list_editable = ("is_active", "order")
