from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('api.auth_urls')),  # Auth endpoints: register, login, token refresh
    path('api/v1/users/', include('api.user_urls')),  # User endpoints (e.g. /me/)
]