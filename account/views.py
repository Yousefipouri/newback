from django.contrib.auth import get_user_model
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserLoginSerializer, UserRegisterSerializer
from .models import OTP
import logging

logger = logging.getLogger(__name__)

# ------------------ Login View ------------------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            user = get_user_model().objects.get(username=ser.validated_data.get('username'))

            if not user.check_password(ser.validated_data.get('password')):
                raise ValueError('رمز عبور نادرست است')
        except Exception:
            return Response({'msg': 'هیچ حساب فعالی با این مشخصات یافت نشد.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': str(token),
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
        }, status=status.HTTP_200_OK)


# ------------------ Register View ------------------
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        
        # Log the incoming request data
        logger.info(f"Incoming registration request: {request.data}")

        # Ensure that OTP was verified before allowing registration
        if not OTP.objects.filter(phone_number=phone_number).exists():
            return Response({
                'error': 'لطفا قبل از ثبت نام شماره تلفن خود را تایید کنید.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        
        # Log validation errors
        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # If validation is successful
        self.perform_create(serializer)

        # After successful registration, delete the OTP record
        OTP.objects.filter(phone_number=phone_number).delete()

        headers = self.get_success_headers(serializer.data)
        return Response({'msg': "ثبت نام با موفقیت انجام شد!"}, status=status.HTTP_201_CREATED, headers=headers)


# ------------------ Logout View ------------------

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
   