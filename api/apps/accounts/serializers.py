from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import User, AllowedEmail, OTPCode
import random
import string
from datetime import timedelta
from django.utils import timezone


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Parollar mos kelmaydi")

        email = attrs["email"]
        if not AllowedEmail.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Bu email manzil tizimda ro'yxatdan o'tmagan"
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        allowed_email = (
            AllowedEmail.objects.filter(email=validated_data["email"])
            .order_by("-created_at")
            .first()
        )
        if not allowed_email:
            raise serializers.ValidationError(
                "Bu email manzil tizimda ro'yxatdan o'tmagan"
            )
        user = User.objects.create_user(
            username=validated_data["email"], role=allowed_email.role, **validated_data
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not User.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError("Foydalanuvchi topilmadi yoki bloklangan")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Email yoki parol noto'g'ri")

        attrs["user"] = user
        return attrs


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = (attrs.get("email") or "").strip().lower()
        code = (attrs.get("code") or "").strip()

        if not code:
            raise serializers.ValidationError("OTP kodni kiriting")

        try:
            otp = OTPCode.objects.filter(
                email__iexact=email,
                code=code,
                used=False,
                expires_at__gt=timezone.now(),
            ).first()

            if not otp:
                raise serializers.ValidationError(
                    "Noto'g'ri yoki muddati o'tgan OTP kod"
                )

            if otp.attempts >= settings.OTP_MAX_ATTEMPTS:
                raise serializers.ValidationError(
                    "OTP kod uchun maksimal urinishlar soni oshirildi"
                )

            attrs["otp"] = otp
            attrs["email"] = email
            attrs["code"] = code

        except OTPCode.DoesNotExist:
            raise serializers.ValidationError("OTP kod topilmadi")

        return attrs


class AllowedEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedEmail
        fields = ("id", "email", "role", "added_by", "created_at")
        read_only_fields = ("added_by", "created_at")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "is_active",
            "created_at",
        )
        read_only_fields = ("role", "created_at")
