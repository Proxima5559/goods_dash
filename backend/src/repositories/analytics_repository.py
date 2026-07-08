from sqlalchemy import case, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.product import Product
from src.models.user import User


class AnalyticsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_monthly_revenue(self):
        month = func.to_char(Order.created_at, "YYYY-MM").label("month")
        stmt = (
            select(month, func.coalesce(func.sum(Order.total), 0).label("revenue"))
            .group_by(month)
            .order_by(month)
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get_orders_by_status(self):
        stmt = (
            select(Order.status, func.count(Order.id).label("count"))
            .group_by(Order.status)
            .order_by(func.count(Order.id).desc())
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get_orders_by_country(self):
        stmt = (
            select(User.country, func.count(Order.id).label("orders"))
            .join(Order, Order.user_id == User.id)
            .group_by(User.country)
            .order_by(func.count(Order.id).desc())
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get_monthly_registrations(self):
        month = func.to_char(User.created_at, "YYYY-MM").label("month")
        stmt = (
            select(month, func.count(User.id).label("users"))
            .group_by(month)
            .order_by(month)
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get_top_products(self, limit: int = 10):
        revenue = func.coalesce(func.sum(OrderItem.price * OrderItem.quantity), 0).label("revenue")
        stmt = (
            select(
                Product.id,
                Product.name,
                Product.category,
                func.count(OrderItem.id).label("orders_count"),
                func.coalesce(func.sum(OrderItem.quantity), 0).label("units_sold"),
                revenue,
            )
            .join(OrderItem, OrderItem.product_id == Product.id)
            .group_by(Product.id)
            .order_by(revenue.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get_category_sales(self):
        revenue = func.coalesce(func.sum(OrderItem.price * OrderItem.quantity), 0).label("revenue")
        stmt = (
            select(
                Product.category,
                revenue,
                func.coalesce(func.sum(OrderItem.quantity), 0).label("units_sold"),
            )
            .join(OrderItem, OrderItem.product_id == Product.id)
            .group_by(Product.category)
            .order_by(revenue.desc())
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get_payment_method_stats(self):
        stmt = (
            select(
                Order.payment_method,
                func.count(Order.id).label("count"),
                func.coalesce(func.sum(Order.total), 0).label("revenue"),
            )
            .group_by(Order.payment_method)
            .order_by(func.count(Order.id).desc())
        )
        result = await self.session.execute(stmt)
        return result.all()

    async def get_revenue_heatmap(self):
        raw_dow = extract("dow", Order.created_at)
        weekday = case(
            (raw_dow == 0, 6),
            else_=raw_dow - 1,
        ).label("weekday")
        hour = extract("hour", Order.created_at).label("hour")

        stmt = (
            select(
                weekday,
                hour,
                func.coalesce(func.sum(Order.total), 0).label("revenue"),
                func.count(Order.id).label("orders_count"),
            )
            .group_by(weekday, hour)
            .order_by(weekday, hour)
        )
        result = await self.session.execute(stmt)
        return result.all()
