from fastapi import APIRouter, Depends, Query

from src.dependencies.dependencies import get_analytics_service
from src.schemes.analytics import (
    CategorySales,
    HeatmapCell,
    MonthlyRevenuePoint,
    MonthlyUserCount,
    OrderCountryCount,
    OrderStatusCount,
    PaymentMethodStats,
    TopProductItem,
)
from src.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/revenue/monthly", response_model=list[MonthlyRevenuePoint])
async def get_monthly_revenue(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_monthly_revenue()


@router.get("/orders/status", response_model=list[OrderStatusCount])
async def get_orders_by_status(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_orders_by_status()


@router.get("/orders/country", response_model=list[OrderCountryCount])
async def get_orders_by_country(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_orders_by_country()


@router.get("/users/monthly", response_model=list[MonthlyUserCount])
async def get_monthly_registrations(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_monthly_registrations()


@router.get("/top-products", response_model=list[TopProductItem])
async def get_top_products(
    limit: int = Query(10, ge=1, le=50),
    service: AnalyticsService = Depends(get_analytics_service),
):
    return await service.get_top_products(limit=limit)


@router.get("/category-sales", response_model=list[CategorySales])
async def get_category_sales(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_category_sales()


@router.get("/payment-methods", response_model=list[PaymentMethodStats])
async def get_payment_method_stats(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_payment_method_stats()


@router.get("/revenue/heatmap", response_model=list[HeatmapCell])
async def get_revenue_heatmap(service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_revenue_heatmap()
