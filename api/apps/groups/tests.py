from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.groups.models import Group, Enrollment
from apps.students.models import Student
from apps.payments.models import Payment

User = get_user_model()


class GroupDetailSerializerTest(TestCase):
    def setUp(self):
        self.boss = User.objects.create_user(
            username="boss@test.com",
            email="boss@test.com",
            password="testpass123",
            role="BOSS",
        )
        self.mentor = User.objects.create_user(
            username="mentor@test.com",
            email="mentor@test.com",
            password="testpass123",
            role="MENTOR",
        )
        self.group = Group.objects.create(
            name="Detail group",
            subject="Math",
            start_date="2024-01-01",
            end_date="2024-12-31",
            mentor=self.mentor,
            price_per_month=Decimal("1000000"),
        )
        self.student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            email="detail-student@test.com",
            phone="+998901234568",
        )
        Enrollment.objects.create(group=self.group, student=self.student)
        self.client = APIClient()

    def test_group_detail_includes_enrollments(self):
        self.client.force_authenticate(self.boss)
        response = self.client.get(f"/api/v1/groups/{self.group.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("enrollments", response.data)
        self.assertEqual(len(response.data["enrollments"]), 1)

    def test_group_detail_falls_back_to_payments(self):
        Enrollment.objects.all().delete()
        Payment.objects.create(
            student=self.student,
            group=self.group,
            amount=Decimal("250000"),
            due_date="2024-03-01",
            status=Payment.Status.PAID,
        )

        self.client.force_authenticate(self.boss)
        response = self.client.get(f"/api/v1/groups/{self.group.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["students_count"], 1)
        self.assertEqual(len(response.data["enrollments"]), 1)
