from django.urls import path
from .views import (
    CreateContentCreatorProfileView,
    UpdateContentCreatorProfileView,
    CreateReaderProfileView,
    UpdateReaderProfileView,
    ContentCreatorProfileDetailView,
    ReaderProfileDetailView
)


urlpatterns = [
    path('content-creator/profile/create/', CreateContentCreatorProfileView.as_view(), name='create-content-creator-profile'),
    path('profile/update/', UpdateContentCreatorProfileView.as_view(), name='update-content-creator-profile'),
    path('reader/profile/create/', CreateReaderProfileView.as_view(), name='create-reader-profile'),
    path('reader/profile/update/', UpdateReaderProfileView.as_view(), name='update-reader-profile'),
    path('content-creator-profile/', ContentCreatorProfileDetailView.as_view(), name='content-creator-profile'),
    path('reader-profile/', ReaderProfileDetailView.as_view(), name='reader-profile'),
]