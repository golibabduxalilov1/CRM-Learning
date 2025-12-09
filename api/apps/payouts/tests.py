from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.groups.models import Group
from apps.payments.models import Payment, CommissionSetting
from apps.payouts.models import MentorPayout
from apps.payouts.services import PayoutService
from apps.students.models import Student

User = get_user_model()


class PayoutTest(TestCase):
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
            phone="123456789",
        )

        self.group = Group.objects.create(
            name="Test Group",
            subject="Math",
            start_date="2024-01-01",
            end_date="2024-12-31",
            mentor=self.mentor,
            price_per_month=Decimal("1000000"),
        )
        self.client = APIClient()

    def _create_paid_payment(
        self,
        amount=Decimal("1000000"),
        paid_at="2024-01-15",
        due_date="2024-01-31",
    ):
        return Payment.objects.create(
            student=self.student,
            group=self.group,
            amount=amount,
            due_date=due_date,
            status="PAID",
            paid_at=paid_at,
        )

    def test_payout_calculation_default_commission(self):
        CommissionSetting.objects.create(
            type="GLOBAL",
            mentor_percentage=Decimal("60.00"),
            center_percentage=Decimal("40.00"),
        )

        Payment.objects.create(
            student=self.student,
            group=self.group,
            amount=Decimal("1000000"),
            due_date="2024-01-31",
            status="PAID",
            paid_at="2024-01-15",
        )

        calculation = PayoutService.calculate_mentor_payout(self.mentor, 2024, 1)

        self.assertEqual(calculation["total_collected"], Decimal("1000000"))
        self.assertEqual(calculation["mentor_share"], Decimal("600000"))
        self.assertEqual(calculation["center_share"], Decimal("400000"))

    def test_generate_payout_and_filter_by_status(self):
        self._create_paid_payment()
        self.client.force_authenticate(self.boss)

        response = self.client.post(
            "/api/v1/payouts/mentor/generate/",
            data={"mentor_id": self.mentor.id, "month": "2024-01"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        payout_id = response.data["payout"]["id"]

        list_response = self.client.get(
            "/api/v1/payouts/mentor/", {"status": MentorPayout.Status.CALCULATED}
        )
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data["count"], 1)
        self.assertEqual(list_response.data["results"][0]["id"], payout_id)

    def test_calculation_uses_due_date_month(self):
        late_payment = self._create_paid_payment(
            amount=Decimal("700000"),
            due_date="2024-02-29",
            paid_at="2024-03-15",
        )

        calculation = PayoutService.calculate_mentor_payout(self.mentor, 2024, 2)
        self.assertEqual(calculation["total_collected"], late_payment.amount)

        march_calc = PayoutService.calculate_mentor_payout(self.mentor, 2024, 3)
        self.assertEqual(march_calc["total_collected"], Decimal("0.00"))

    def test_mark_payout_paid_and_detail_breakdown(self):
        self._create_paid_payment(amount=Decimal("500000"))
        payout = PayoutService.generate_payout(self.mentor, 2024, 1)

        self.client.force_authenticate(self.boss)
        response = self.client.patch(
            f"/api/v1/payouts/mentor/{payout.id}/paid/",
            data={"payment_details": {"method": "bank", "ref": "TX123"}},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        payout.refresh_from_db()
        self.assertEqual(payout.status, MentorPayout.Status.PAID)
        self.assertIsNotNone(payout.paid_at)
        self.assertEqual(payout.payment_details.get("method"), "bank")

        detail_response = self.client.get(f"/api/v1/payouts/mentor/{payout.id}/")
        self.assertEqual(detail_response.status_code, 200)
        self.assertIn("payment_breakdown", detail_response.data)
        self.assertGreaterEqual(len(detail_response.data["payment_breakdown"]), 1)
