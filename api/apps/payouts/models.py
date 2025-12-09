from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class MentorPayout(TimeStampedModel):
    class Status(models.TextChoices):
        CALCULATED = "CALCULATED", "Hisoblangan"
        PAID = "PAID", "To'langan"
        CANCELLED = "CANCELLED", "Bekor qilingan"

    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "MENTOR"}
    )
    month = models.DateField()
    total_collected = models.DecimalField(max_digits=12, decimal_places=2)
    mentor_share = models.DecimalField(max_digits=12, decimal_places=2)
    center_share = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.CALCULATED
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_details = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("mentor", "month")
