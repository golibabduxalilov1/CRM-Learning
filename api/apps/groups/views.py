from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Group, Enrollment
from .serializers import GroupSerializer, EnrollmentSerializer, GroupDetailSerializer
from apps.core.permissions import IsBossOrAdmin, MentorCanViewOwnGroups


User = get_user_model()


class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsBossOrAdmin]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [MentorCanViewOwnGroups()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.role in ["SUPERADMIN", "BOSS", "ADMIN"]:
            return Group.objects.select_related("mentor").all()
        elif user.role == "MENTOR":
            return Group.objects.filter(mentor=user)
        return Group.objects.none()


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer
    permission_classes = [IsBossOrAdmin]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [MentorCanViewOwnGroups()]
        return [permission() for permission in self.permission_classes]


class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.select_related("student", "group").all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsBossOrAdmin]


class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsBossOrAdmin]


@api_view(["POST"])
@permission_classes([IsBossOrAdmin])
def assign_mentor(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        mentor_id = request.data.get("mentor_id")

        mentor = User.objects.get(id=mentor_id, role="MENTOR")
        group.mentor = mentor
        group.save()

        return Response(
            {
                "message": "Mentor muvaffaqiyatli tayinlandi",
                "group": GroupSerializer(group).data,
            }
        )

    except Group.DoesNotExist:
        return Response({"error": "Guruh topilmadi"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({"error": "Mentor topilmadi"}, status=status.HTTP_404_NOT_FOUND)
