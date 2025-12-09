from decimal import Decimal
from datetime import date
from ..payments.models import Payment, CommissionSetting
from .models import MentorPayout


class PayoutService:
    ROUNDING = Decimal("0.01")

    @staticmethod
    def get_commission_percentage(mentor, group=None):
        if group:
            try:
                setting = CommissionSetting.objects.get(
                    type="GROUP", group=group, is_active=True
                )
                return setting.mentor_percentage
            except CommissionSetting.DoesNotExist:
                pass

        try:
            setting = CommissionSetting.objects.get(
                type="MENTOR", mentor=mentor, is_active=True
            )
            return setting.mentor_percentage
        except CommissionSetting.DoesNotExist:
            pass

        try:
            setting = CommissionSetting.objects.get(type="GLOBAL", is_active=True)
            return setting.mentor_percentage
        except CommissionSetting.DoesNotExist:
            return Decimal("60.00")

    @staticmethod
    def _get_month_range(year: int, month: int):
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        return start_date, end_date

    @classmethod
    def _quantize(cls, amount: Decimal) -> Decimal:
        return (amount or Decimal("0")).quantize(cls.ROUNDING)

    @classmethod
    def calculate_mentor_payout(cls, mentor, year, month):
        start_date, end_date = cls._get_month_range(year, month)

        payments = (
            Payment.objects.filter(
                group__mentor=mentor,
                status=Payment.Status.PAID,
                due_date__gte=start_date,
                due_date__lt=end_date,
            ).select_related("group")
        )

        total_collected = Decimal("0.00")
        mentor_share = Decimal("0.00")

        for payment in payments:
            commission_pct = cls.get_commission_percentage(mentor, payment.group)
            payment_mentor_share = payment.amount * (commission_pct / 100)

            total_collected += payment.amount
            mentor_share += payment_mentor_share

        total_collected = cls._quantize(total_collected)
        mentor_share = cls._quantize(mentor_share)
        center_share = cls._quantize(total_collected - mentor_share)

        return {
            "total_collected": total_collected,
            "mentor_share": mentor_share,
            "center_share": center_share,
        }

    @classmethod
    def generate_payout(cls, mentor, year, month):
        month_date = date(year, month, 1)
        calculation = cls.calculate_mentor_payout(mentor, year, month)

        existing_payout = MentorPayout.objects.filter(
            mentor=mentor, month=month_date
        ).first()

        if existing_payout:
            should_update = existing_payout.status != MentorPayout.Status.PAID

            if existing_payout.status == MentorPayout.Status.PAID:
                should_update = (
                    existing_payout.total_collected == 0
                    and calculation["total_collected"] > 0
                ) or (
                    existing_payout.mentor_share == 0
                    and calculation["mentor_share"] > 0
                )

            if should_update:
                existing_payout.total_collected = calculation["total_collected"]
                existing_payout.mentor_share = calculation["mentor_share"]
                existing_payout.center_share = calculation["center_share"]

                update_fields = [
                    "total_collected",
                    "mentor_share",
                    "center_share",
                    "updated_at",
                ]

                if existing_payout.status != MentorPayout.Status.PAID:
                    existing_payout.status = MentorPayout.Status.CALCULATED
                    update_fields.append("status")

                existing_payout.save(update_fields=update_fields)

            return existing_payout

        payout = MentorPayout.objects.create(
            mentor=mentor,
            month=month_date,
            total_collected=calculation["total_collected"],
            mentor_share=calculation["mentor_share"],
            center_share=calculation["center_share"],
        )

        return payout
