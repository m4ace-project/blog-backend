from rest_framework import serializers
from .models import ContentCreatorProfile, ReaderProfile

class ContentCreatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCreatorProfile
        fields = ['profile_id', 'user', 'name', 'username', 'profile_pic', 'bio', 'created_at', 'updated_at']
        read_only_fields = ['profile_id', 'user', 'created_at', 'updated_at']

        def create(self, validated_data):
            return ContentCreatorProfile.objects.create(**validated_data)
        

        def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        
class ReaderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderProfile
        fields = ['reader_id', 'user', 'profile_pic', 'name', 'username', 'bio', 'created_at', 'updated_at']
        read_only_fields = ['reader_id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        return ReaderProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance