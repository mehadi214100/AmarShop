from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_link', 'quantity', 'price', 'get_cost')
    can_delete = False

    def product_link(self, obj):
        if obj.product:
            url = f"/admin/shop/product/{obj.product.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return '-'
    product_link.short_description = "Product"

    def get_cost(self, obj):
        return (obj.quantity or 0) * (obj.price or 0)
    get_cost.short_description = "Total"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone', 'status', 'total_price', 'paid', 'created_at')
    list_display_links = ('id', 'user', 'full_name', 'phone', 'status', 'total_price') 
    list_filter = ('status', 'paid', 'created_at')
    search_fields = ('user__username', 'full_name', 'email', 'phone')
    inlines = [OrderItemInline]
    readonly_fields = ('transaction_id', 'created_at', 'total_price')
