from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Payment, CommissionSetting
from .serializers import PaymentSerializer, CommissionSettingSerializer
from apps.core.permissions import IsBossOrAdmin, IsSuperAdminOrBoss


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsBossOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "group", "student"]
    search_fields = [
        "student__first_name",
        "student__last_name",
        "group__name",
        "amount",
    ]
    ordering_fields = ["created_at", "due_date", "amount"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.role in ["SUPERADMIN", "BOSS", "ADMIN"]:
            return (
                Payment.objects.select_related("student", "group")
                .all()
                .order_by("-created_at")
            )
        elif user.role == "MENTOR":
            return Payment.objects.filter(group__mentor=user)
        return Payment.objects.none()


class PaymentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsBossOrAdmin]


@api_view(["PATCH"])
@permission_classes([IsBossOrAdmin])
def update_payment_status(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        new_status = request.data.get("status")

        if new_status == "PAID" and payment.status != "PAID":
            payment.paid_at = timezone.now()

        payment.status = new_status
        payment.notes = request.data.get("notes", payment.notes)
        payment.payment_method = request.data.get(
            "payment_method", payment.payment_method
        )
        payment.save()

        return Response(
            {
                "message": "To'lov holati yangilandi",
                "payment": PaymentSerializer(payment).data,
            }
        )
    except Payment.DoesNotExist:
        return Response({"error": "To'lov topilmadi"}, status=status.HTTP_404_NOT_FOUND)


class CommissionGlobalView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSuperAdminOrBoss]
    serializer_class = CommissionSettingSerializer

    def get_object(self):
        obj, created = CommissionSetting.objects.get_or_create(
            type="GLOBAL", defaults={"mentor_percentage": 60, "center_percentage": 40}
        )
        return obj


@api_view(["PUT"])
@permission_classes([IsBossOrAdmin])
def update_group_commission(request, group_id):
    from apps.groups.models import Group

    try:
        group = Group.objects.get(id=group_id)
        commission, created = CommissionSetting.objects.get_or_create(
            type="GROUP", group=group
        )

        serializer = CommissionSettingSerializer(
            commission, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Group.DoesNotExist:
        return Response({"error": "Guruh topilmadi"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@permission_classes([IsBossOrAdmin])
def update_mentor_commission(request, mentor_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        mentor = User.objects.get(id=mentor_id, role="MENTOR")
        commission, created = CommissionSetting.objects.get_or_create(
            type="MENTOR", mentor=mentor
        )

        serializer = CommissionSettingSerializer(
            commission, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "Mentor topilmadi"}, status=status.HTTP_404_NOT_FOUND)
