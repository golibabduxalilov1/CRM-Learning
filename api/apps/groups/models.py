from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import SoftDeleteModel
from apps.students.models import Student

User = get_user_model()


class Group(SoftDeleteModel):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    mentor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, limit_choices_to={"role": "MENTOR"}
    )
    max_students = models.PositiveIntegerField(default=20)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Enrollment(SoftDeleteModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Faol"
        PAUSED = "PAUSED", "To'xtatilgan"
        COMPLETED = "COMPLETED", "Tugatilgan"
        DROPPED = "DROPPED", "Tashlab ketgan"

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )

    class Meta:
        unique_together = ("student", "group")
