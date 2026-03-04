from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_analytics_service
from app.schemas.analytics import AlertsResponse, DashboardSummary, MonthlyReport
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_dashboard_summary()


@router.get("/monthly-report", response_model=MonthlyReport)
def monthly_report(
    year: int = Query(default=datetime.now().year, ge=2020),
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    service: AnalyticsService = Depends(get_analytics_service),
):
    return service.get_monthly_report(year=year, month=month)


@router.get("/alerts", response_model=AlertsResponse)
def alerts(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_alerts()
