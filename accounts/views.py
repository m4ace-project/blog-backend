import random
from django.utils.timezone import now, timedelta
from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, OneTimePassword
from .serializers import UserRegisterSerializer, LoginSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, LogoutUserSerializer
from rest_framework import status
from .utils import send_otp_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer
    
    def post(self, request):
        user_data= request.data
        serializer=self.serializer_class(data=user_data)
        
        if serializer.is_valid():
            user = serializer.save()

            # Generate a 6-digit OTP
            otp_code = random.randint(1000, 9999)
            expiration_time = now() + timedelta(minutes=60)

            #  Save OPT in the database
            OneTimePassword.objects.create(user=user, otp=otp_code, expires_at = expiration_time)

            # Send the OTP via email
            send_otp_email(user.email, otp_code)

            return Response({
                'data': serializer.data,
                'message': "Hi! Thanks for signing up. An OTP has been sent to your email for verification."
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Email verification using OTP
class VerifyUserEmail(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        
        if not otp:
            return Response({
                'message': 'OTP is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve the OTP record
            otp_record = OneTimePassword.objects.get(otp=otp)

            # Check if OTP has expired
            if otp_record.expires_at < now():
                return Response({
                    'message': 'OPT has expired'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Mark the associated user as verified
            user = otp_record.user
            if not user.is_verified:
                user.is_verified = True
                user.save()

            # Delet the OTP record after successful verification
            otp_record.delete()

            return Response({
                'message': 'Account email verified successfully. You can proceed to login'
            }, status=status.HTTP_200_OK)
        
        except OneTimePassword.DoesNotExist:
            return Response({
                'message': 'Invalid or expired OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
        


class LoginUserView(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordResetRequestView(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
    

class PasswordResetConfirm(GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'Token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK) 
    
        except DjangoUnicodeDecodeError as identifier:
            return Response({'message':'Token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
    

class SetNewPasswordView(GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success':True, 'message':'Paasword reset is successful'}, status=status.HTTP_200_OK)


class LogoutApiView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

