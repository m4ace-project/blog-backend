from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, TestView


urlpatterns=[
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='Login'),
    # This url is for testing authenticated/protected views
    path('test/', TestView.as_view(), name='test'),
]