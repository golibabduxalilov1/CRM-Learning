from django.db import models
from django.utils import timezone
from decimal import Decimal
from apps.core.models import TimeStampedModel
from apps.students.models import Student
from apps.groups.models import Group


class Payment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Kutilmoqda"
        PAID = "PAID", "To'langan"
        OVERDUE = "OVERDUE", "Muddati o'tgan"
        CANCELLED = "CANCELLED", "Bekor qilingan"

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.amount} - {self.status}"

    def save(self, *args, **kwargs):
        """
        Ensure paid_at always reflects the moment a payment enters the PAID state.
        This keeps payout calculations reliable even if payments are created or
        updated outside the REST serializers.
        """
        if self.status == self.Status.PAID and self.paid_at is None:
            self.paid_at = timezone.now()
        elif self.status != self.Status.PAID and self.paid_at is not None:
            self.paid_at = None
        super().save(*args, **kwargs)


class CommissionSetting(TimeStampedModel):
    class Type(models.TextChoices):
        GLOBAL = "GLOBAL", "Global"
        GROUP = "GROUP", "Guruh"
        MENTOR = "MENTOR", "Mentor"

    type = models.CharField(max_length=10, choices=Type.choices)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)
    mentor = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"role": "MENTOR"},
    )
    mentor_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("60.00")
    )
    center_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("40.00")
    )
    is_active = models.BooleanField(default=True)
