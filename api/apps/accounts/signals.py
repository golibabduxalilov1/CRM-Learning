from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from apps.core.models import AuditLog
from .models import User, AllowedEmail
from apps.notifications.utils import send_notification


@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            user=instance,
            action="CREATE",
            model_name="User",
            object_id=str(instance.id),
            details={"role": instance.role, "email": instance.email},
        )


@receiver(post_save, sender=AllowedEmail)
def log_allowlist_changes(sender, instance, created, **kwargs):
    action = "CREATE" if created else "UPDATE"
    AuditLog.objects.create(
        user=instance.added_by,
        action=action,
        model_name="AllowedEmail",
        object_id=str(instance.id),
        details={"email": instance.email, "role": instance.role},
    )


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action="LOGIN",
        model_name="User",
        object_id=str(user.id),
        ip_address=request.META.get("REMOTE_ADDR"),
    )
