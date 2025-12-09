from django.urls import path
from . import views

urlpatterns = [
    path("", views.GroupListCreateView.as_view(), name="group-list"),
    path("<int:pk>/", views.GroupDetailView.as_view(), name="group-detail"),
    path("<int:group_id>/assign-mentor/", views.assign_mentor, name="assign-mentor"),
    path(
        "enrollments/", views.EnrollmentListCreateView.as_view(), name="enrollment-list"
    ),
    path(
        "enrollments/<int:pk>/",
        views.EnrollmentDetailView.as_view(),
        name="enrollment-detail",
    ),
]
