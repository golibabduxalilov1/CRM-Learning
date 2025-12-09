from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import User, AllowedEmail, OTPCode
from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    OTPVerificationSerializer,
    AllowedEmailSerializer,
    UserSerializer,
)
from apps.core.permissions import IsSuperAdmin, CanManageAllowlist


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "Ro'yxatdan o'tish muvaffaqiyatli", "user_id": user.id},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]

        code = "".join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(seconds=settings.OTP_TTL)

        email = user.email.strip().lower()

        OTPCode.objects.create(email=email, code=code, expires_at=expires_at)

        send_mail(
            "Training CRM - OTP Kod",
            f"Sizning OTP kodingiz: {code}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response(
            {"message": "OTP kod emailingizga yuborildi", "email": user.email}
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        otp = serializer.validated_data["otp"]
        user = User.objects.get(email__iexact=otp.email)

        otp.used = True
        otp.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get("refresh")

    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            # Even if token is invalid/expired we still end the session gracefully.
            pass

    return Response({"message": "Tizimdan muvaffaqiyatli chiqdingiz"})


class AllowedEmailListCreateView(generics.ListCreateAPIView):
    permission_classes = [CanManageAllowlist]
    serializer_class = AllowedEmailSerializer

    def get_queryset(self):
        return AllowedEmail.objects.select_related("added_by").all()

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class AllowedEmailDestroyView(generics.DestroyAPIView):
    queryset = AllowedEmail.objects.all()
    permission_classes = [CanManageAllowlist]

    def perform_destroy(self, instance):
        request_user = self.request.user

        if request_user.role == "BOSS" and instance.role not in ["ADMIN", "MENTOR"]:
            raise PermissionDenied("Boss faqat admin yoki mentorni o'chira oladi.")

        related_user = User.objects.filter(
            email__iexact=instance.email, role=instance.role
        ).first()

        super().perform_destroy(instance)

        if request_user.role == "BOSS" and instance.role in ["ADMIN", "MENTOR"]:
            if related_user:
                related_user.delete()


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        role = self.kwargs.get("role")
        if role:
            return User.objects.filter(role=role.upper(), is_active=True)
        return User.objects.filter(is_active=True)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
