from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateUserAPIView, RetrieveUpdateDestroyUserAPIView

urlpatterns = [
    path('login/token/', TokenObtainPairView.as_view(), name='obtain_token_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('create-user/', CreateUserAPIView.as_view(), name='create_user'),
    path('user/<str:username>/', RetrieveUpdateDestroyUserAPIView.as_view(), name='user'),
]
