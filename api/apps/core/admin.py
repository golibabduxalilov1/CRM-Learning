from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = (
        "user",
        "action",
        "model_name",
        "object_id",
        "created_at",
        "ip_address",
    )
    list_filter = ("action", "model_name", "created_at")
    search_fields = ("user__username", "model_name", "object_id", "details")
    date_hierarchy = "created_at"
    readonly_fields = (
        "user",
        "action",
        "model_name",
        "object_id",
        "details",
        "created_at",
        "ip_address",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
