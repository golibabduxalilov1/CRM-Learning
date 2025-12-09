from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.cache import cache
from datetime import datetime
from .services import AnalyticsService
from apps.core.permissions import IsSuperAdminBossOrAdmin


@api_view(["GET"])
@permission_classes([IsSuperAdminBossOrAdmin])
def revenue_summary(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    cache_key = f"revenue_summary_{start_date}_{end_date}"
    data = cache.get(cache_key)

    if not data:
        data = AnalyticsService.get_revenue_summary(start_date, end_date)
        cache.set(cache_key, data, 300)

    return Response(data)


@api_view(["GET"])
@permission_classes([IsSuperAdminBossOrAdmin])
def monthly_revenue_chart(request):
    months = int(request.GET.get("months", 12))

    cache_key = f"monthly_revenue_{months}"
    data = cache.get(cache_key)

    if not data:
        data = AnalyticsService.get_monthly_revenue_chart(months)
        cache.set(cache_key, data, 600)

    return Response(data)


@api_view(["GET"])
@permission_classes([IsSuperAdminBossOrAdmin])
def students_per_group(request):
    cache_key = "students_per_group"
    data = cache.get(cache_key)

    if not data:
        data = AnalyticsService.get_students_per_group()
        cache.set(cache_key, data, 300)

    return Response(data)


@api_view(["GET"])
@permission_classes([IsSuperAdminBossOrAdmin])
def mentor_performance(request):
    cache_key = "mentor_performance"
    data = cache.get(cache_key)

    if not data:
        data = AnalyticsService.get_mentor_performance()
        cache.set(cache_key, data, 600)

    return Response(data)


@api_view(["GET"])
@permission_classes([IsSuperAdminBossOrAdmin])
def payment_status_distribution(request):
    cache_key = "payment_status_distribution"
    data = cache.get(cache_key)

    if not data:
        data = list(AnalyticsService.get_payment_status_distribution())
        cache.set(cache_key, data, 300)

    return Response(data)


@api_view(["GET"])
@permission_classes([IsSuperAdminBossOrAdmin])
def enrollment_trends(request):
    days = int(request.GET.get("days", 30))

    cache_key = f"enrollment_trends_{days}"
    data = cache.get(cache_key)

    if not data:
        data = AnalyticsService.get_enrollment_trends(days)
        cache.set(cache_key, data, 300)

    return Response(data)
