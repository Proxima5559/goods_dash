from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.order import Order
from src.models.product import Product
from src.models.user import User


class DashboardRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_total_users(self) -> int:
        stmt = select(func.count(User.id))

        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def get_vip_users(self) -> int:
        stmt = (
            select(func.count(User.id))
            .where(User.vip.is_(True))
        )

        result = await self.session.execute(stmt)

        return result.scalar_one()
    
    async def get_total_orders(self) -> int:
        stmt = select(func.count(Order.id))

        result = await self.session.execute(stmt)

        return result.scalar_one()
    
    async def get_total_revenue(self):
        stmt = (
            select(
                func.coalesce(func.sum(Order.total), 0)
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one()
    
    async def get_average_order(self):
        stmt = (
            select(
                func.coalesce(func.avg(Order.total), 0)
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one()
    
    async def get_total_products(self):
        stmt = select(func.count(Product.id))

        result = await self.session.execute(stmt)

        return result.scalar_one()
    async def get_low_stock_products(self):
        stmt = (
            select(func.count(Product.id))
            .where(Product.stock < 10)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one()