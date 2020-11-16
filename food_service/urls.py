from django.urls import path

from .views import ListCreateFoodAPIView, ListCreateOrderAPIView

urlpatterns = [
    path('food/', ListCreateFoodAPIView.as_view(), name='food'),
    path('order/', ListCreateOrderAPIView.as_view(), name='order')
]
