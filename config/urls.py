from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView  # Import TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('api.auth_urls')),  # Auth endpoints: register, login
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/users/', include('api.user_urls')),  # User endpoints (e.g. /me/)
]
