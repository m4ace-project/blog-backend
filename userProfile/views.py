from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import ContentCreatorProfile
from .serializers import ContentCreatorProfileSerializer


class CreateContentCreatorProfileView(generics.CreateAPIView):
    queryset = ContentCreatorProfile.objects.all()
    serializer_class = ContentCreatorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateContentCreatorProfileView(generics.UpdateAPIView):
    queryset = ContentCreatorProfile.objects.all()
    serializer_class = ContentCreatorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure that the user can only update their own profile
        return ContentCreatorProfile.objects.get(user=self.request.user)
    
    