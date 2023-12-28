from rest_framework import serializers
from .models import User, UserManager
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=15, min_length=8)
    password_confirm = serializers.CharField(write_only=True, max_length=15, min_length=8)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        password_confirm = attrs.get('password_confirm', '')

        if not password.isalnum():
            raise serializers.ValidationError('The password should only contain alphanumeric characters')
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Password mismatch')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=15, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username, password=password)

        return {
            'username': user.username,
            'tokens': user.tokens()
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'avatar',
                  'date_of_birth',
                  'phone_number']

class VerificationSerializer(serializers.ModelSerializer):
     verify_code = serializers.CharField(min_length=4, required=True)


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']



