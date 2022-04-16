from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create(self, username, email, password):
        if not username:
            raise ValueError('User must have a username')
        if not email:
            raise ValueError('User must have a email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create(username, email, password)
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, *_):
        return self.is_staff

    def has_module_perms(self, *_):
        return self.is_staff