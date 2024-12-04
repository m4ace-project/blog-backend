from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import ContentCreatorProfile, ReaderProfile
from .serializers import ContentCreatorProfileSerializer, ReaderProfileSerializer

# Create Content Creator Profile
class CreateContentCreatorProfileView(generics.CreateAPIView):
    queryset = ContentCreatorProfile.objects.all()
    serializer_class = ContentCreatorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        # Check if a profile already exists for the user
        if ContentCreatorProfile.objects.filter(user=self.request.user).exists():
            raise PermissionDenied("You already have a content creator profile.")

        if self.request.user.role != 'content_creator':
            raise PermissionDenied("Only content creators can create this profile")
        serializer.save(user=self.request.user)


# Update Content Creator Profile
class UpdateContentCreatorProfileView(generics.UpdateAPIView):
    queryset = ContentCreatorProfile.objects.all()
    serializer_class = ContentCreatorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure that the user can only update their own profile
        return ContentCreatorProfile.objects.get(user=self.request.user)
    

class CreateReaderProfileView(generics.CreateAPIView):
    queryset = ReaderProfile.objects.all()
    serializer_class = ReaderProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        # Check if a profile already exists for the user
        if ReaderProfile.objects.filter(user=self.request.user).exists():
            raise PermissionDenied("You already have a reader profile.")

        if self.request.user.role != 'reader':
            raise PermissionDenied("Only readers can create this profile.")
        serializer.save(user=self.request.user)


# Update Reader Profile
class UpdateReaderProfileView(generics.UpdateAPIView):
    queryset = ReaderProfile.objects.all()
    serializer_class = ReaderProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure the user can only update their own profile
        return ReaderProfile.objects.get(user=self.request.user)


class ContentCreatorProfileDetailView(generics.RetrieveAPIView):
    queryset = ContentCreatorProfile.objects.all()
    serializer_class = ContentCreatorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retrieve the profile for the currently authenticated user
        return ContentCreatorProfile.objects.get(user=self.request.user)
    

class ReaderProfileDetailView(generics.RetrieveAPIView):
    queryset = ReaderProfile.objects.all()
    serializer_class = ReaderProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retrieve the profile for the currently authenticated user
        return ReaderProfile.objects.get(user=self.request.user)
    