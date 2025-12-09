from rest_framework import serializers
from .models import Group, Enrollment
from apps.students.serializers import StudentSerializer


class GroupSerializer(serializers.ModelSerializer):
    mentor_name = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "subject",
            "description",
            "start_date",
            "end_date",
            "mentor",
            "mentor_name",
            "max_students",
            "price_per_month",
            "students_count",
            "created_at",
            "updated_at",
            "is_deleted",
            "deleted_at",
        )
        read_only_fields = ("created_at", "updated_at", "is_deleted", "deleted_at")

    def get_mentor_name(self, obj):
        return f"{obj.mentor.first_name} {obj.mentor.last_name}" if obj.mentor else None

    def get_students_count(self, obj):
        active_enrollments = obj.enrollment_set.filter(
            status="ACTIVE", is_deleted=False
        ).count()
        if active_enrollments:
            return active_enrollments

        from apps.payments.models import Payment

        return (
            Payment.objects.filter(group=obj, student__isnull=False)
            .values("student_id")
            .distinct()
            .count()
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = "__all__"
        read_only_fields = ("enrolled_date", "created_at", "updated_at")

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def get_group_name(self, obj):
        return obj.group.name


class GroupDetailSerializer(GroupSerializer):
    enrollments = serializers.SerializerMethodField()

    class Meta(GroupSerializer.Meta):
        fields = tuple(GroupSerializer.Meta.fields) + ("enrollments",)

    def get_enrollments(self, obj):
        enrollments = (
            obj.enrollment_set.filter(is_deleted=False)
            .select_related("student")
            .all()
        )

        if enrollments.exists():
            return EnrollmentSerializer(enrollments, many=True).data

        from apps.payments.models import Payment

        payments = (
            Payment.objects.filter(group=obj, student__isnull=False)
            .select_related("student")
            .order_by("student__first_name", "student__last_name")
        )

        fallback = {}
        for payment in payments:
            student = payment.student
            if not student or student.id in fallback:
                continue

            fallback[student.id] = {
                "id": f"payment-student-{student.id}",
                "student": student.id,
                "student_name": f"{student.first_name} {student.last_name}",
                "group": obj.id,
                "group_name": obj.name,
                "status": Enrollment.Status.ACTIVE,
                "enrolled_date": payment.paid_at.date()
                if payment.paid_at
                else payment.due_date,
                "created_at": payment.created_at,
                "updated_at": payment.updated_at,
            }

        return list(fallback.values())
