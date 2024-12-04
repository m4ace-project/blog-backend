from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _ 
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

# Create your models here.

AUTH_PROVIDERS = {'email':'email', 'google':'google', 'facebook':'facebook'}

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('content_creator', 'Content Creator'),
        ('reader', 'Reader'),
    )
    id = models.BigAutoField(primary_key=True, editable=False)
    email=models.EmailField(max_length=254, unique=True, verbose_name=_("Email Address"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get('email'))
    
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    USERNAME_FIELD = "email"
    
    
    
    objects = UserManager()    
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
    def __str__(self):
        return self.email
    
    
class OneTimePassword(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification_tokens")
    otp = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
