from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path("create_order/", views.create_order, name="create_order"),
    path('payment-process/<int:order_id>/', views.payment_process, name='payment_process'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-fail/', views.payment_fail, name='payment_fail'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),    
    path('payment-success', views.payment_success),
    path('payment-fail', views.payment_fail),
    path('payment-cancel', views.payment_cancel),
]
