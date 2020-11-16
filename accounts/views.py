from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics, permissions, exceptions, response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsAccountOwner
from .serializers import UserSerializer

User = get_user_model()


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def create(self, request, *args, **kwargs):
        account_type = request.GET.get('account_type')
        if account_type == 'buyer' or account_type == 'seller':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.groups.add(Group.objects.get_or_create(name=account_type)[0])
            headers = self.get_success_headers(data=serializer.data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            raise exceptions.ValidationError({'account_type': 'only buyer or seller account is allowed'})


class RetrieveUpdateDestroyUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAccountOwner,
    ]
    authentication_classes = [
        JWTAuthentication,
    ]
    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        response_dict = serializer.data
        response_dict['is_buyer'] = user.is_buyer
        response_dict['is_seller'] = user.is_seller
        return response.Response(response_dict)
