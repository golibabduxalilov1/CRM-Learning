from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.students.models import Student
from apps.groups.models import Group, Enrollment
from apps.payments.models import Payment

User = get_user_model()


class MentorStudentAccessTest(TestCase):
    def setUp(self):
        self.mentor = User.objects.create_user(
            username="mentor@test.com",
            email="mentor@test.com",
            password="testpass123",
            role="MENTOR",
        )
        self.boss = User.objects.create_user(
            username="boss@test.com",
            email="boss@test.com",
            password="testpass123",
            role="BOSS",
        )
        self.student = Student.objects.create(
            first_name="Test",
            last_name="Student",
            email="student@test.com",
            phone="+998901234567",
        )
        self.group = Group.objects.create(
            name="Test group",
            subject="Math",
            start_date="2024-01-01",
            end_date="2024-12-31",
            mentor=self.mentor,
            price_per_month=Decimal("1000000"),
        )
        Enrollment.objects.create(student=self.student, group=self.group)
        self.client = APIClient()

    def test_mentor_sees_only_linked_students(self):
        other_student = Student.objects.create(
            first_name="Other",
            last_name="Student",
            email="other@test.com",
            phone="+998907654321",
        )
        other_group = Group.objects.create(
            name="Other group",
            subject="Science",
            start_date="2024-01-01",
            end_date="2024-12-31",
            mentor=self.boss,
            price_per_month=Decimal("900000"),
        )
        Enrollment.objects.create(student=other_student, group=other_group)

        self.client.force_authenticate(self.mentor)
        response = self.client.get("/api/v1/students/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.student.id)

    def test_mentor_sees_students_with_payments_even_without_enrollment(self):
        for enrollment in self.group.enrollment_set.all():
            enrollment.delete()
        Payment.objects.create(
            student=self.student,
            group=self.group,
            amount=Decimal("500000"),
            due_date="2024-02-01",
            status=Payment.Status.PAID,
            paid_at="2024-02-05",
        )

        self.client.force_authenticate(self.mentor)
        response = self.client.get("/api/v1/students/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.student.id)
