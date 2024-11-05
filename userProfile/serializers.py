from rest_framework import serializers
from .models import ContentCreatorProfile

class ContentCreatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCreatorProfile
        fields = ['profile_id', 'user', 'name', 'profile_pic', 'bio', 'niches', 'created_at', 'updated_at']
        read_only_fields = ['profile_id', 'user', 'created_at', 'updated_at']

        def create(self, validated_data):
            return ContentCreatorProfile.objects.create(**validated_data)
        

        def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance