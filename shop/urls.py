from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("all_products/",views.all_products,name="all_products"),
    path("all_products/<slug:category>/",views.all_products,name="category_products"),
    path("product_details/<slug:product_name>/",views.product_details,name="product_details"),
]
