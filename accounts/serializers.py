import json
from dataclasses import field
from .models import User
from userProfile.models import ContentCreatorProfile, ReaderProfile
from rest_framework import serializers
from string import ascii_lowercase, ascii_uppercase
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_otp_email, send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2=serializers.CharField(max_length=68, min_length=6, write_only=True)
    role = serializers.ChoiceField(choices=[('content_creator', 'Content Creator'), ('reader', 'Reader')])
    
    class Meta:
        model=User
        fields=['email', 'password', 'password2', 'role']
        
    def validate(self, attrs):
        password= attrs.get('password', '')
        password2= attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError('passwords do not match')
        return attrs
    
    
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )        
        return user
    
            
class LoginSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(max_length=155, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    role = serializers.CharField(read_only=True)   
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)
    name = serializers.SerializerMethodField()
    


    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'access_token', 'refresh_token', 'name']
    
    def get_name(self, obj):
        user = obj if isinstance(obj, User) else None
        if user:
            profile = None
            if user.role == 'content_creator':
                profile = ContentCreatorProfile.objects.filter(user=user).first()
            elif user.role == 'reader':
                profile = ReaderProfile.objects.filter(user=user).first()
            return profile.name if profile else None

    def validate(self, attrs):        
        email = attrs.get('email')
        password = attrs.get('password')        
        request= self.context.get('request')
        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials try again")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        
        self.context['user'] = user
        return user
    
    def to_representation(self, instance):
        user = instance
        profile = None
        if  user.role == 'content_creator':
            profile = ContentCreatorProfile.objects.filter(user=user).first()
        elif user.role == 'reader':
            profile = ReaderProfile.objects.filter(user=user).first()

        tokens = user.tokens()

        return {
            'id':user.id,
            'email':user.email,
            'role':user.role,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh')),
            "name": profile.name if profile else None,
        }
          
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            current_site = get_current_site(request).domain
            relative_link = reverse('reset-password-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abslink = f"http://{current_site}{relative_link}"
            print(abslink)
            email_body = f"Hi {user.email} use the link below to reset your password \n {abslink}"
            data = {
                'email_body':email_body,
                'email_subject':"Reset your Password",
                'to_email':user.email
            }
            send_normal_email(data)
            
        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)
    token=serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields= ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset link is invalid or has expired", 401)
            

            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match")
              
            attrs['user'] = user
            return attrs
        
        except User.DoesNotExist:
            return AuthenticationFailed("User not found", 404)
        
    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()
        return user
class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_message= {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')

        return attrs 

    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return  self.fail('bad_token')
        

    
