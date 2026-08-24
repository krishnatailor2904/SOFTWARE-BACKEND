from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def health_check(request):
    """
    GET / -> sirf ye confirm karne ke liye ki backend zinda hai aur
    deploy sahi se hua hai. Frontend isko call nahi karta.
    """
    return JsonResponse({'status': 'ok', 'service': 'tailor-shop-backend'})


urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('billing.urls')),
]
