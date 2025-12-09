import django_filters
from .models import Student
from apps.groups.models import Group


class StudentFilter(django_filters.FilterSet):
    group = django_filters.ModelChoiceFilter(
        queryset=Group.objects.all(),
        field_name="enrollment__group",
    )
    enrollment_status = django_filters.CharFilter(field_name="enrollment__status")
    created_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
    )

    class Meta:
        model = Student
        fields = ["group", "enrollment_status", "created_after"]
