from rest_framework import serializers
from django.utils import timezone
from .models import Payment, CommissionSetting


class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def get_group_name(self, obj):
        return obj.group.name

    def _attach_current_user(self, instance):
        request = self.context.get("request")
        if request and getattr(request, "user", None) and request.user.is_authenticated:
            instance._current_user = request.user

    def _set_paid_timestamp(self, instance, new_status, provided_paid_at=None, previous_status=None):
        if provided_paid_at is not None:
            instance.paid_at = provided_paid_at
            return

        if new_status == Payment.Status.PAID:
            if previous_status != Payment.Status.PAID or not instance.paid_at:
                instance.paid_at = timezone.now()
        elif previous_status == Payment.Status.PAID and new_status != Payment.Status.PAID:
            instance.paid_at = None

    def create(self, validated_data):
        status = validated_data.get("status", Payment.Status.PENDING)
        paid_at = validated_data.get("paid_at")
        instance = Payment(**validated_data)
        self._set_paid_timestamp(instance, status, provided_paid_at=paid_at, previous_status=None)
        self._attach_current_user(instance)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        previous_status = instance.status
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if "status" in validated_data or "paid_at" in validated_data:
            self._set_paid_timestamp(
                instance,
                validated_data.get("status", instance.status),
                provided_paid_at=validated_data.get("paid_at", None),
                previous_status=previous_status,
            )
        self._attach_current_user(instance)
        instance.save()
        return instance


class CommissionSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionSetting
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        mentor_pct = attrs.get("mentor_percentage", 0)
        center_pct = attrs.get("center_percentage", 0)

        if mentor_pct + center_pct != 100:
            raise serializers.ValidationError(
                "Mentor va markaz foizlari yig'indisi 100% bo'lishi kerak"
            )
        return attrs
