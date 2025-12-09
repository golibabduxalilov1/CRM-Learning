from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Payment, CommissionSetting


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = (
        "student",
        "group",
        "amount",
        "due_date",
        "status",
        "paid_at",
        "payment_method",
    )
    list_filter = ("status", "payment_method", "due_date")
    search_fields = (
        "student__first_name",
        "student__last_name",
        "group__name",
        "notes",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(CommissionSetting)
class CommissionSettingAdmin(ModelAdmin):
    list_display = (
        "type",
        "group",
        "mentor",
        "mentor_percentage",
        "center_percentage",
        "is_active",
    )
    list_filter = ("type", "is_active")
    search_fields = ("group__name", "mentor__first_name", "mentor__last_name")
