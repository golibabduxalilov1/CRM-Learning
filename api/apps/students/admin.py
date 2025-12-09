from django.contrib import admin
from .models import Student
from unfold.admin import ModelAdmin


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "birth_date",
        "is_deleted",
    )
    list_filter = ("is_deleted", "birth_date")
    search_fields = ("first_name", "last_name", "email", "phone")
    ordering = ("last_name", "first_name")
    list_per_page = 25
