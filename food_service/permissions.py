from rest_framework import permissions


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        else:
            return request.user.is_seller or request.method in permissions.SAFE_METHODS


class IsBuyerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if self.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        else:
            return request.user.is_buyer or request.method in permissions.SAFE_METHODS
