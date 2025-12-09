from django.urls import path
from . import views

urlpatterns = [
    path("mentor/", views.MentorPayoutListView.as_view(), name="mentor-payout-list"),
    path(
        "mentor/<int:pk>/",
        views.MentorPayoutDetailView.as_view(),
        name="mentor-payout-detail",
    ),
    path("mentor/generate/", views.generate_mentor_payout, name="generate-payout"),
    path(
        "mentor/<int:payout_id>/paid/", views.mark_payout_paid, name="mark-payout-paid"
    ),
]
