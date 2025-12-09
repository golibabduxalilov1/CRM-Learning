from rest_framework import serializers
from .models import Student
from apps.groups.models import Enrollment


class StudentSerializer(serializers.ModelSerializer):
    enrollments_count = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "address",
            "emergency_contact",
            "is_active",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
            "enrollments_count",
        ]
        read_only_fields = ("created_at", "updated_at", "is_deleted", "deleted_at")

    def get_enrollments_count(self, obj):
        request = self.context.get("request")
        queryset = obj.enrollment_set.filter(status="ACTIVE")

        if request and getattr(request, "user", None) and request.user.role == "MENTOR":
            queryset = queryset.filter(group__mentor=request.user)

        return queryset.count()


class StudentDetailSerializer(StudentSerializer):
    enrollments = serializers.SerializerMethodField()

    class Meta(StudentSerializer.Meta):
        fields = StudentSerializer.Meta.fields + ["enrollments"]

    def get_enrollments(self, obj):
        from apps.groups.serializers import EnrollmentSerializer

        request = self.context.get("request")
        enrollments = obj.enrollment_set.select_related("group").all()

        if request and getattr(request, "user", None) and request.user.role == "MENTOR":
            enrollments = enrollments.filter(group__mentor=request.user)

        return EnrollmentSerializer(enrollments, many=True).data
