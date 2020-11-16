from rest_framework import generics, mixins
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Food, Order
from .pagination import PageSize10Pagination
from .permissions import IsSellerOrReadOnly, IsBuyerOrReadOnly
from .serializers import BuyerFoodSerializer, SellerFoodSerializer, OrderSerializer


class ListCreateFoodAPIView(generics.ListAPIView, mixins.CreateModelMixin):
    permission_classes = [IsSellerOrReadOnly, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = PageSize10Pagination

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_seller:
                return SellerFoodSerializer
        return BuyerFoodSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_seller:
                return Food.objects.filter(seller=self.request.user)
        return Food.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            if self.request.user.is_seller:
                serializer.save(seller=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListCreateOrderAPIView(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = OrderSerializer
    permission_classes = [IsBuyerOrReadOnly, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = PageSize10Pagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_buyer:
                return Order.objects.filter(buyer=self.request.user)
        return []

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            if self.request.user.is_buyer:
                serializer.save(buyer=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
