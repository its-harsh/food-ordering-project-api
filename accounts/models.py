from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models

from .validators import UsernameValidator, EmailValidator


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username and not email:
            raise ValueError('Users must have an email and a username.')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Username', max_length=15, unique=True, validators=[UsernameValidator(), ],
        help_text='Required. 15 characters, Only a-z, A-Z, 0-9 and (.), (_), (-) are allowed.'
    )
    email = models.EmailField(
        verbose_name='Email', max_length=254, unique=True, validators=[EmailValidator(), ],
        help_text='Allowed email address domains [ gmail.com, icloud.com, outlook.com, protonmail.com, yahoo.com ].'
    )
    is_active = models.BooleanField(verbose_name='Active', default=True)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)
    is_superuser = models.BooleanField(verbose_name='Superuser', default=False)
    last_login = None

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    @property
    def is_buyer(self):
        try:
            if Group.objects.get(name='buyer') in self.groups.all():
                return True
        except Group.DoesNotExist:
            pass
        return False

    @property
    def is_seller(self):
        try:
            if Group.objects.get(name='seller') in self.groups.all():
                return True
        except Group.DoesNotExist:
            pass
        return False
