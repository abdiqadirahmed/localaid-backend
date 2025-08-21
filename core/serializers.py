from rest_framework import serializers
from .models import AidRequest, DonatedResource
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class AidRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AidRequest
        fields = ['id', 'user', 'user_email', 'category', 'description', 'is_resolved', 'created_at']
        read_only_fields = ['user', 'created_at']


class DonatedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonatedResource
        fields = '__all__'
        read_only_fields = ['donor', 'is_claimed', 'created_at', 'latitude', 'longitude']


class AidRequestAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AidRequest
        fields = ['id', 'user', 'user_email', 'category', 'description', 'is_resolved', 'is_flagged', 'created_at']
        read_only_fields = ['user', 'created_at']


class DonatedResourceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonatedResource
        fields = ['id', 'donor', 'title', 'description', 'category', 'location', 'is_claimed', 'is_flagged', 'created_at']
        read_only_fields = ['donor', 'created_at']