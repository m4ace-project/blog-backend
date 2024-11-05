from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, OneTimePassword
from .serializers import UserRegisterSerializer, LoginSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, LogoutUserSerializer
from rest_framework import status
from .utils import send_verification_email
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

            # Generate a unique verification token
            token_obj = OneTimePassword.objects.create(user=user)

            # Send the email with the verification email link
            send_verification_email(user.email, token_obj.token)

            return Response({
                'data': serializer.data,
                'message': "Hi! Thanks for signing up, use the link sent to your email to verify your account."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyUserEmail(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'message': 'Verification token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve user with the matching token
            user_pass_obj = OneTimePassword.objects.get(token=token)
            user = user_pass_obj.user

            if not user.is_verified:
                # Mark the user as verified
                user.is_verified = True
                user.save()



                return Response({'message': 'Account email verified successfully, you can proceed to login'}, status=status.HTTP_200_OK)

        except OneTimePassword.DoesNotExist:
            return Response({'message': 'Invalid or expired verification link'}, status=status.HTTP_400_BAD_REQUEST)
        

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
    

