from django.urls import path
from .views import UserDetailAPIView

urlpatterns = [
    path('me/', UserDetailAPIView.as_view(), name='user-detail'),
]
