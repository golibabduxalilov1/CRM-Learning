from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import MentorPayout
from .serializers import (
    MentorPayoutSerializer,
    MentorPayoutDetailSerializer,
    PayoutGenerationSerializer,
    PayoutStatusUpdateSerializer,
)
from .services import PayoutService
from apps.core.permissions import IsBossOrAdmin, IsSuperAdminOrBoss

User = get_user_model()


class MentorPayoutListView(generics.ListAPIView):
    serializer_class = MentorPayoutSerializer

    def get_queryset(self):
        user = self.request.user
        mentor_id = self.request.query_params.get("mentor_id")
        base_queryset = MentorPayout.objects.select_related("mentor")

        if user.role in ["SUPERADMIN", "BOSS", "ADMIN"]:
            queryset = base_queryset
            if mentor_id:
                queryset = queryset.filter(mentor_id=mentor_id)
        elif user.role == "MENTOR":
            queryset = base_queryset.filter(mentor=user)
        else:
            queryset = MentorPayout.objects.none()

        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)

        month_param = self.request.query_params.get("month")
        if month_param:
            try:
                year, month = map(int, month_param.split("-"))
                month_date = datetime(year, month, 1).date()
                queryset = queryset.filter(month=month_date)
            except ValueError:
                pass

        return queryset.order_by("-month", "-created_at")


class MentorPayoutDetailView(generics.RetrieveAPIView):
    serializer_class = MentorPayoutDetailSerializer

    def get_queryset(self):
        user = self.request.user
        base_queryset = MentorPayout.objects.select_related("mentor")

        if user.role in ["SUPERADMIN", "BOSS", "ADMIN"]:
            return base_queryset
        if user.role == "MENTOR":
            return base_queryset.filter(mentor=user)
        return MentorPayout.objects.none()


@api_view(["POST"])
@permission_classes([IsBossOrAdmin])
def generate_mentor_payout(request):
    serializer = PayoutGenerationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    mentor_id = serializer.validated_data["mentor_id"]
    month_param = serializer.validated_data["month"]

    try:
        mentor = User.objects.get(id=mentor_id, role="MENTOR")
        year, month = map(int, month_param.split("-"))

        payout = PayoutService.generate_payout(mentor, year, month)

        return Response(
            {
                "message": "Mentor to'lovi hisoblandi",
                "payout": MentorPayoutSerializer(payout).data,
            }
        )
    except User.DoesNotExist:
        return Response({"error": "Mentor topilmadi"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response(
            {"error": "Noto'g'ri sana formati"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PATCH"])
@permission_classes([IsSuperAdminOrBoss])
def mark_payout_paid(request, payout_id):
    payout = get_object_or_404(MentorPayout, id=payout_id)
    update_payload = {
        "status": MentorPayout.Status.PAID,
        "payment_details": request.data.get("payment_details", {}),
    }

    serializer = PayoutStatusUpdateSerializer(
        instance=payout, data=update_payload, partial=True
    )
    serializer.is_valid(raise_exception=True)

    status_changed = payout.status != MentorPayout.Status.PAID
    payout.status = MentorPayout.Status.PAID
    if status_changed or payout.paid_at is None:
        payout.paid_at = timezone.now()
    payout.payment_details = serializer.validated_data.get(
        "payment_details", payout.payment_details
    )
    payout.save(update_fields=["status", "paid_at", "payment_details", "updated_at"])

    return Response(
        {
            "message": "To'lov holati yangilandi",
            "payout": MentorPayoutSerializer(payout).data,
        }
    )
