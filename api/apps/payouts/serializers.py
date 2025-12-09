from rest_framework import serializers
from decimal import Decimal
from .models import MentorPayout
from django.contrib.auth import get_user_model

User = get_user_model()


class MentorPayoutSerializer(serializers.ModelSerializer):
    mentor_name = serializers.SerializerMethodField()
    month_display = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = MentorPayout
        fields = [
            "id",
            "mentor",
            "mentor_name",
            "month",
            "month_display",
            "total_collected",
            "mentor_share",
            "center_share",
            "status",
            "status_display",
            "paid_at",
            "payment_details",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "total_collected",
            "mentor_share",
            "center_share",
            "created_at",
            "updated_at",
        ]

    def get_mentor_name(self, obj):
        return f"{obj.mentor.first_name} {obj.mentor.last_name}"

    def get_month_display(self, obj):
        return obj.month.strftime("%Y yil %B")


class MentorPayoutDetailSerializer(MentorPayoutSerializer):
    mentor_details = serializers.SerializerMethodField()
    payment_breakdown = serializers.SerializerMethodField()

    class Meta(MentorPayoutSerializer.Meta):
        fields = MentorPayoutSerializer.Meta.fields + [
            "mentor_details",
            "payment_breakdown",
        ]

    def get_mentor_details(self, obj):
        return {
            "id": obj.mentor.id,
            "email": obj.mentor.email,
            "phone": getattr(obj.mentor, "phone", ""),
            "role": obj.mentor.role,
        }

    def get_payment_breakdown(self, obj):
        from apps.payments.models import Payment
        from datetime import datetime

        year = obj.month.year
        month = obj.month.month

        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()

        payments = Payment.objects.filter(
            group__mentor=obj.mentor,
            status=Payment.Status.PAID,
            due_date__gte=start_date,
            due_date__lt=end_date,
        ).select_related("student", "group")

        breakdown = []
        for payment in payments:
            from apps.payouts.services import PayoutService

            commission_pct = PayoutService.get_commission_percentage(
                obj.mentor, payment.group
            )
            mentor_amount = payment.amount * (commission_pct / 100)

            breakdown.append(
                {
                    "payment_id": payment.id,
                    "student_name": f"{payment.student.first_name} {payment.student.last_name}",
                    "group_name": payment.group.name,
                    "total_amount": payment.amount,
                    "commission_percentage": commission_pct,
                    "mentor_amount": mentor_amount,
                    "paid_at": payment.paid_at,
                }
            )

        return breakdown


class PayoutGenerationSerializer(serializers.Serializer):
    mentor_id = serializers.IntegerField()
    month = serializers.CharField(max_length=7, help_text="Format: YYYY-MM")

    def validate_mentor_id(self, value):
        try:
            mentor = User.objects.get(id=value, role="MENTOR", is_active=True)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Faol mentor topilmadi")

    def validate_month(self, value):
        try:
            year, month = map(int, value.split("-"))
            if month < 1 or month > 12:
                raise ValueError()
            return value
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "Noto'g'ri sana formati. YYYY-MM formatida kiriting"
            )


class PayoutStatusUpdateSerializer(serializers.Serializer):
    STATUS_CHOICES = [
        ("CALCULATED", "Hisoblangan"),
        ("PAID", "To'langan"),
        ("CANCELLED", "Bekor qilingan"),
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    payment_details = serializers.JSONField(required=False, default=dict)

    def validate_status(self, value):
        instance = self.instance
        if instance and instance.status == "PAID" and value != "PAID":
            raise serializers.ValidationError(
                "To'langan to'lovni boshqa holatga o'zgartirib bo'lmaydi"
            )
        return value
