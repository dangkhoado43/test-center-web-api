from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_admin', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }
        
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data.pop('password'))  # Hash the password
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar']

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_admin', 'avatar']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_id"] = self.user.id
        data["username"] = self.user.username
        return data

class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "phone", "is_active", "is_staff"]
        read_only_fields = ["email", "is_active", "is_staff"]
