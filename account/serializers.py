from rest_framework import serializers
from django.core.exceptions import ValidationError

from . import models


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MyUser
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'phone_number',
        ]

    def validate_phone_number(self, value):
        if len(value) != 11 or not value.startswith('09'):
            raise ValidationError("شماره تلفن باید ۱۱ رقمی باشد و با '09' شروع شود.")
        
        if models.MyUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("این شماره تلفن قبلاً ثبت شده است.")

        return value



    def validate_username(self, value):
        """Check if the username already exists"""
        
        if models.MyUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("این نام کاربری قبلاً ثبت شده است.")
        return value

    

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.MyUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
