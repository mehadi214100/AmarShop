from django.urls import path
from . import views

urlpatterns = [
    path('',views.profile,name="profile"),
    path('settings/',views.settings,name="settings"),
    path('viewWishlist/',views.viewWishlist,name="viewWishlist"),
    path('myorders/',views.myorders,name="myorders"),
    path('removeWishlist/<int:item_id>/',views.removeWishlist,name="removeWishlist"),
]
