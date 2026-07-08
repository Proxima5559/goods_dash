from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import BaseRepository
from src.models.order import Order, OrderStatus, PaymentMethod
from src.models.order_item import OrderItem
from src.models.user import User
from src.schemes.filters import OrderSortField

ORDER_SORT_COLUMNS = {
    OrderSortField.CREATED_AT: Order.created_at,
    OrderSortField.TOTAL: Order.total,
    OrderSortField.STATUS: Order.status,
    OrderSortField.SHIPPED_AT: Order.shipped_at,
    OrderSortField.DELIVERED_AT: Order.delivered_at,
}


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Order, session=session)

    def _filtered_query(
        self,
        *,
        status: OrderStatus | None = None,
        country: str | None = None,
        vip: bool | None = None,
        payment: PaymentMethod | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        search: str | None = None,
    ):
        stmt = select(Order).join(User, Order.user_id == User.id)

        filters = [
            Order.status == status if status is not None else None,
            User.country == country if country else None,
            User.vip == vip if vip is not None else None,
            Order.payment_method == payment if payment is not None else None,
            Order.created_at >= date_from if date_from else None,
            Order.created_at <= date_to if date_to else None,
            or_(User.name.ilike(f"%{search}%"), User.email.ilike(f"%{search}%")) if search else None
        ]

        active_filters = [f for f in filters if f is not None]
        if active_filters:
            stmt = stmt.where(and_(*active_filters))

        return stmt

    async def get_orders_filtered(
        self,
        *,
        page: int,
        page_size: int,
        status: OrderStatus | None = None,
        country: str | None = None,
        vip: bool | None = None,
        payment: PaymentMethod | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        search: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> tuple[list[Order], int]:
        filter_keys = {"status", "country", "vip", "payment", "date_from", "date_to", "search"}
        query_params = {k: v for k, v in locals().items() if k in filter_keys}
        
        base_stmt = self._filtered_query(**query_params)

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        sort_column = ORDER_SORT_COLUMNS.get(sort, Order.created_at)
        stmt = (
            base_stmt.options(selectinload(Order.user))
            .order_by(sort_column.desc() if order == "desc" else sort_column.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_order_detail(self, order_id: UUID) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.user),
                selectinload(Order.items).selectinload(OrderItem.product),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()