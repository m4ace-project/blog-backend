from django.urls import path
from . import views


urlpatterns = [
    path('profile/create/', views.CreateContentCreatorProfileView.as_view(), name='create-profile'),
    path('profile/update/', views.UpdateContentCreatorProfileView.as_view(), name='update-profile'),
]