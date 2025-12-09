from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import Student
from .serializers import StudentSerializer, StudentDetailSerializer
from .filters import StudentFilter
from apps.core.permissions import IsBossAdminOrMentorReadOnly


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.select_related().all()
    serializer_class = StudentSerializer
    permission_classes = [IsBossAdminOrMentorReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentFilter
    search_fields = ["first_name", "last_name", "email", "phone"]
    ordering_fields = ["created_at", "first_name", "last_name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        base_qs = super().get_queryset()

        if user.role == "MENTOR":
            mentor_filter = Q(enrollment__group__mentor=user) | Q(
                payment__group__mentor=user
            )
            return base_qs.filter(mentor_filter).distinct()

        return base_qs


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    permission_classes = [IsBossAdminOrMentorReadOnly]

    def get_queryset(self):
        user = self.request.user
        base_qs = super().get_queryset()

        if user.role == "MENTOR":
            mentor_filter = Q(enrollment__group__mentor=user) | Q(
                payment__group__mentor=user
            )
            return base_qs.filter(mentor_filter).distinct()

        return base_qs
