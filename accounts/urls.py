from django.urls import path
from .views import (
    RegisterUserView, 
    VerifyUserEmail, 
    LoginUserView, 
    TestView,
    PasswordResetConfirm,
    PasswordResetRequestView,
    SetNewPasswordView,
    LogoutApiView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('login/', LoginUserView.as_view(), name='Login'),
    # This url is for testing authenticated/protected views
    path('test/', TestView.as_view(), name='test'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='reset-password-confirm'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('logout/', LogoutApiView.as_view(), name='logout'),

]