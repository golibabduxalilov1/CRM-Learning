from django.urls import path
from . import views

urlpatterns = [
    path("revenue/", views.revenue_summary, name="revenue-summary"),
    path("revenue/monthly/", views.monthly_revenue_chart, name="monthly-revenue"),
    path("students-per-group/", views.students_per_group, name="students-per-group"),
    path("mentor-performance/", views.mentor_performance, name="mentor-performance"),
    path("payment-status/", views.payment_status_distribution, name="payment-status"),
    path("enrollment-trends/", views.enrollment_trends, name="enrollment-trends"),
]
