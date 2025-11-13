from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('profile/', include('profileApp.urls')),
    path('order/', include(('order.urls', 'order'), namespace='order')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if not settings.DEBUG:
    from django.views.static import serve
    urlpatterns += [
        path('static/<path:path>/', serve, {'document_root': settings.STATIC_ROOT}),
        path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT})
    ]

from django.conf.urls import handler404, handler500, handler403, handler400
from django.shortcuts import render

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '404.html', status=500)

def custom_403(request, exception=None):
    return render(request, '404.html', status=403)

def custom_400(request, exception=None):
    return render(request, '404.html', status=400)

handler404 = custom_404
handler500 = custom_500
handler403 = custom_403
handler400 = custom_400
