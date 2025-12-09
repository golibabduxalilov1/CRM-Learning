from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "SUPERADMIN"


class IsBoss(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "BOSS"


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "MENTOR"


class IsBossOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["BOSS", "ADMIN"]


class IsSuperAdminOrBoss(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "SUPERADMIN",
            "BOSS",
        ]


class IsAdminOrMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "ADMIN",
            "MENTOR",
        ]


class CanManageAllowlist(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role == "SUPERADMIN":
            return True

        # Boss can verify admin and mentor roles
        target_role = request.data.get("role") if request.method == "POST" else None
        if user.role == "BOSS" and target_role in ["ADMIN", "MENTOR"]:
            return True

        return False


class MentorCanViewOwnGroups(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role in ["SUPERADMIN", "BOSS", "ADMIN"]:
            return True
        elif request.user.role == "MENTOR":
            if hasattr(obj, "mentor"):
                return obj.mentor == request.user
            elif hasattr(obj, "group"):
                return obj.group.mentor == request.user

        return False
