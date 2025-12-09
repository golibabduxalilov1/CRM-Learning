from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import MentorPayout


@admin.register(MentorPayout)
class MentorPayoutAdmin(ModelAdmin):
    list_display = (
        "mentor",
        "month",
        "total_collected",
        "mentor_share",
        "center_share",
        "status",
        "paid_at",
    )
    list_filter = ("status", "month")
    search_fields = ("mentor__first_name", "mentor__last_name")
    date_hierarchy = "month"
    ordering = ("-month", "-created_at")
