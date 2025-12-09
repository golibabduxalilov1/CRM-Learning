from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "SUPERADMIN"


class IsBoss(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "BOSS"


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


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


class IsSuperAdminBossOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "SUPERADMIN",
            "BOSS",
            "ADMIN",
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

        if user.role == "BOSS":
            if request.method == "POST":
                target_role = request.data.get("role")
                return target_role in ["ADMIN", "MENTOR"]

            # Allow bosses to list/delete existing entries
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


class IsBossAdminOrMentorReadOnly(BasePermission):
    """
    Boss/Admin have full access, mentors can only perform safe (read) operations.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role in ["SUPERADMIN", "BOSS", "ADMIN"]:
            return True

        if request.user.role == "MENTOR" and request.method in SAFE_METHODS:
            return True

        return False
