from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from apps.core.models import AuditLog
from apps.notifications.utils import send_notification, send_dashboard_update
from apps.groups.models import Enrollment


@receiver(post_save, sender=Payment)
def log_payment_changes(sender, instance, created, **kwargs):
    action = "CREATE" if created else "UPDATE"
    user = getattr(instance, "_current_user", None)
    if user:
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name="Payment",
            object_id=str(instance.id),
            details={
                "student": str(instance.student),
                "amount": str(instance.amount),
                "status": instance.status,
            },
        )

    if instance.status == "PAID" and not created:
        send_notification(
            instance.student.id,
            f"To'lovingiz qabul qilindi: {instance.amount} so'm",
            {"payment_id": instance.id},
        )

        send_dashboard_update(
            {
                "type": "payment_received",
                "amount": str(instance.amount),
                "student": str(instance.student),
            }
        )


@receiver(post_save, sender=Payment)
def ensure_enrollment_exists(sender, instance, **kwargs):
    if not instance.student_id or not instance.group_id:
        return

    enrollment = Enrollment.all_objects.filter(
        student=instance.student, group=instance.group
    ).first()

    if enrollment:
        updates = []
        if enrollment.is_deleted:
            enrollment.is_deleted = False
            enrollment.deleted_at = None
            updates.extend(["is_deleted", "deleted_at"])
        if enrollment.status == Enrollment.Status.DROPPED:
            enrollment.status = Enrollment.Status.ACTIVE
            updates.append("status")

        if updates:
            enrollment.save(update_fields=updates + ["updated_at"])
        return

    Enrollment.objects.create(
        student=instance.student,
        group=instance.group,
        status=Enrollment.Status.ACTIVE,
    )
