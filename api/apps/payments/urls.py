from django.urls import path
from . import views

urlpatterns = [
    path("", views.PaymentListCreateView.as_view(), name="payment-list"),
    path("<int:pk>/", views.PaymentDetailView.as_view(), name="payment-detail"),
    path(
        "<int:payment_id>/status/", views.update_payment_status, name="payment-status"
    ),
    path(
        "commission/global/",
        views.CommissionGlobalView.as_view(),
        name="commission-global",
    ),
    path(
        "commission/group/<int:group_id>/",
        views.update_group_commission,
        name="commission-group",
    ),
    path(
        "commission/mentor/<int:mentor_id>/",
        views.update_mentor_commission,
        name="commission-mentor",
    ),
]
