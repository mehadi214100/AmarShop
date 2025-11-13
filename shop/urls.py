from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("all_products/",views.all_products,name="all_products"),
    path("flash_product/<int:flash_id>",views.flash_product,name="flash_product"),
    path("all_products/<slug:category_wase>/",views.all_products,name="category_products"),
    path("product_details/<slug:product_name>/",views.product_details,name="product_details"),
    path("search_product/",views.search_product,name="search_product"),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
]
