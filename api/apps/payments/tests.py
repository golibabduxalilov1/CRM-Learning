from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.groups.models import Group, Enrollment
from apps.students.models import Student
from .models import Payment

User = get_user_model()


class PaymentEnrollmentSignalTest(TestCase):
    def setUp(self):
        self.mentor = User.objects.create_user(
            username="mentor@test.com",
            email="mentor@test.com",
            password="testpass123",
            role="MENTOR",
        )
        self.student = Student.objects.create(
            first_name="Signal",
            last_name="Student",
            email="signal@student.com",
            phone="+998909999999",
        )
        self.group = Group.objects.create(
            name="Signal group",
            subject="Math",
            start_date="2024-01-01",
            end_date="2024-12-31",
            mentor=self.mentor,
            price_per_month=Decimal("1000000"),
        )

    def _create_payment(self):
        return Payment.objects.create(
            student=self.student,
            group=self.group,
            amount=Decimal("200000"),
            due_date="2024-02-01",
            status=Payment.Status.PAID,
        )

    def test_payment_creates_enrollment(self):
        self._create_payment()
        self.assertTrue(
            Enrollment.objects.filter(student=self.student, group=self.group).exists()
        )

    def test_payment_restores_deleted_enrollment(self):
        enrollment = Enrollment.objects.create(
            student=self.student,
            group=self.group,
            status=Enrollment.Status.DROPPED,
        )
        enrollment.delete()

        self._create_payment()

        enrollment.refresh_from_db()
        self.assertFalse(enrollment.is_deleted)
        self.assertEqual(enrollment.status, Enrollment.Status.ACTIVE)
