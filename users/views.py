from django.shortcuts import render, redirect
from rest_framework import generics, status, permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import *
from config.util import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegistrationView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        #user = User.objects.get(email=user_data['email'])

        #token = RefreshToken.for_user(user).access_token

        #current_site = get_current_site(request).domain
        #relativelink = reverse('email-verify')

        #absurl = 'http://' + current_site + relativelink + "?token=" + str(token)
        #email_body = 'Hi'+user.username+'Use link bellow to verify your email\n'+absurl
        #data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        #Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


# class VerifyEmail(APIView):
#     serializer_class = EmailVerificationSerializer
#
#     token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
#
#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.Get.get('token')
#         try:
#             payload = jwt.decode(token,  settings.SECRET_KEY)
#             user = User.objects.get(id=payload['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#
#             return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
       # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
    # permission_classes = IsAuthenticated

#     def post(self, request):
#
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(status=status.HTTP_204_NO_CONTENT)



