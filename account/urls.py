from django.urls import path
from rest_framework.authtoken import views as rst
from .otp_views import SendOTPView, VerifyOTPView
from . import views


urlpatterns = [
    path('v1/account/login/', views.LoginView.as_view()),
    path('v1/account/register/', views.RegisterView.as_view()),
    path('v1/account/logout/', views.LogoutView.as_view()),  # Logout API

    # OTP routes
    path('v1/account/send-otp/', SendOTPView.as_view()),
    path('v1/account/verify-otp/', VerifyOTPView.as_view()),
]
