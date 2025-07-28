from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.user_register,name="user_register"),
    path("login/",views.user_login,name="user_login"),
    path("verify/<uidb64>/<token>/",views.verify_email, name="verify-email")
]
