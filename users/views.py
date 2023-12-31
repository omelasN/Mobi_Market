from django.shortcuts import render, redirect
from rest_framework import generics, status, permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import *
from allauth.account.models import EmailConfirmation
from allauth.account.utils import complete_signup
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
import random
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({'user_id': user.id, 'access': access, 'refresh': str(refresh)}, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self):
        return self.request.user


class SendCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = PhoneNumberSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        phone_number = serializer.validated_data['phone_number']
        verify_code = ''.join(random.choice('0123456789') for _ in range(4))
        user.verify_code = verify_code
        user.save()

        message = f'Your verification code is:{verify_code}'
        from_email = 'semeteeva.n@gmail.com'
        recipient_list = [serializer.instance.email]

        send_mail(message, from_email, recipient_list)
        return Response(
            {'message': 'The code was sent to your email.'},
            status=status.HTTP_200_OK
        )


class VerificationView(APIView):
    serializer_classes = VerificationSerializer

    def post(self, request):
        user = request.user
        verify_code = request.data.get('verify_code')
        if verify_code == user.verify_code:
            user.is_verified = True
            user.save()
            return Response(
                {'message': 'You verified profile.'}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Enter the correct code.'}, status=status.HTTP_400_BAD_REQUEST
            )



