from django.shortcuts import render,HttpResponse,redirect
from .forms import RegistrationForm
from .utils import send_verification_mail
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import User,userProfile


def user_register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            send_verification_mail(request, user)
            messages.info(request, "We have sent you an verfication email")
            return redirect('user_login')
    else:
        form = RegistrationForm()

    return render(request,'account/registration.html',{'form':form})

def user_login(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request,email=email,password=password)

        if not user:
            messages.error(request, "Invalid email or password.")
        elif not user.is_active:
            messages.error(request, "Your email is not verified yet.")
        else:
            login(request,user)
            messages.success(request, "You have successfully logged in.")
            return redirect("home")

    return render(request,"account/login.html")

def verify_email(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been verified successfully.")
        return redirect("user_login")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("user_register")
    


def user_logout(request):
    logout(request)
    return redirect("user_login")