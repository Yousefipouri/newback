from rest_framework.views import APIView
from rest_framework import permissions, status
from django.http import JsonResponse
from .models import OTP, MyUser
import requests

class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        # Check if phone number already exists in the MyUser model
        if MyUser.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'error': 'این شماره تلفن قبلاً ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        # API URL for sending OTP via third-party service
        api_url = 'https://console.melipayamak.com/api/send/otp/630c0150ae954dc7924a908ca8763548'
        data = {'to': phone_number}

        try:
            # Send the OTP via external SMS service
            response = requests.post(api_url, json=data)
            # print('Status Code:', response.status_code)
            response_data = response.json()
            # print(response_data) 

            if response_data.get('code'):
                # OTP successfully sent, save the OTP code in the database
                otp_code = response_data['code']
                OTP.objects.create(phone_number=phone_number, otp_code=otp_code)
                return JsonResponse({'message': 'کد تایید با موفقیت ارسال شد.'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': 'ارسال کد تایید ناموفق بود.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'خطا در ارسال کد تایید: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JsonResponse({'error': f'خطای غیرمنتظره: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp_code = request.data.get('otp_code')

        try:
            # Check if OTP record exists with the given phone number and OTP code
            otp_record = OTP.objects.get(phone_number=phone_number, otp_code=otp_code)
        except OTP.DoesNotExist:
            return JsonResponse({'error': 'کد تایید یا شماره تلفن نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if OTP is still valid (within 5 minutes)
        if not otp_record.is_valid():
            return JsonResponse({'error': 'کد تایید منقضی شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': 'کد تایید با موفقیت تایید شد.'}, status=status.HTTP_200_OK)
