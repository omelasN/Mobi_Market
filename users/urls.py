from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import *
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
#
#
# class GetMethod:
#     pass
#
#
# router.register('data', GetMethod, basename='data')


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', VerificationView.as_view(), name='verify'),
    path('send/', SendCodeView.as_view(), name='send'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
