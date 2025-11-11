from django.urls import path
from . import views

urlpatterns = [
    path("",views.viewcart,name="cart"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path("remove_cart/<int:item_id>/", views.remove_cart, name="remove_cart"),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('addwishlist/<int:item_id>', views.addwishlist, name='addwishlist'),
    

]
