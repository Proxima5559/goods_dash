from src.core.constants import to_money
from src.repositories.analytics_repository import AnalyticsRepository
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


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository):
        self.repository = repository

    async def get_monthly_revenue(self) -> list[MonthlyRevenuePoint]:
        rows = await self.repository.get_monthly_revenue()
        return [MonthlyRevenuePoint(month=month, revenue=to_money(revenue)) for month, revenue in rows]

    async def get_orders_by_status(self) -> list[OrderStatusCount]:
        rows = await self.repository.get_orders_by_status()
        return [OrderStatusCount(status=status.value, count=count) for status, count in rows]

    async def get_orders_by_country(self) -> list[OrderCountryCount]:
        rows = await self.repository.get_orders_by_country()
        return [OrderCountryCount(country=country, orders=orders) for country, orders in rows]

    async def get_monthly_registrations(self) -> list[MonthlyUserCount]:
        rows = await self.repository.get_monthly_registrations()
        return [MonthlyUserCount(month=month, users=users) for month, users in rows]

    async def get_top_products(self, limit: int = 10) -> list[TopProductItem]:
        rows = await self.repository.get_top_products(limit=limit)
        return [
            TopProductItem(
                id=str(product_id),
                name=name,
                category=category,
                orders_count=orders_count,
                units_sold=units_sold,
                revenue=to_money(revenue),
            )
            for product_id, name, category, orders_count, units_sold, revenue in rows
        ]

    async def get_category_sales(self) -> list[CategorySales]:
        rows = await self.repository.get_category_sales()
        return [
            CategorySales(category=category, revenue=to_money(revenue), units_sold=units_sold)
            for category, revenue, units_sold in rows
        ]

    async def get_payment_method_stats(self) -> list[PaymentMethodStats]:
        rows = await self.repository.get_payment_method_stats()
        return [
            PaymentMethodStats(payment_method=method.value, count=count, revenue=to_money(revenue))
            for method, count, revenue in rows
        ]

    async def get_revenue_heatmap(self) -> list[HeatmapCell]:
        rows = await self.repository.get_revenue_heatmap()
        return [
            HeatmapCell(
                weekday=int(weekday),
                hour=int(hour),
                revenue=to_money(revenue),
                orders_count=orders_count,
            )
            for weekday, hour, revenue, orders_count in rows
        ]
