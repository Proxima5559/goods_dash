from datetime import datetime
from uuid import UUID
 
from sqlalchemy import and_, func, literal_column, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Literal
 
from src.schemes.user import UserSortField
from .base import BaseRepository
from src.models.order import Order
from src.models.user import User


USER_SORT_COLUMNS = {
    UserSortField.NAME: User.name,
    UserSortField.EMAIL: User.email,
    UserSortField.COUNTRY: User.country,
    UserSortField.CREATED_AT: User.created_at,
    UserSortField.TOTAL_SPENT: literal_column("total_spent"),
    UserSortField.ORDERS_COUNT: literal_column("orders_count"),
}

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)
    
    def _base_query(
        self,
        *,
        country: str | None = None,
        vip: bool | None = None,
        created_after: datetime | None = None,
        created_before: datetime | None = None,
        search: str | None = None,
    ):
        stmt = (
            select(
                User,
                func.count(Order.id).label("orders_count"),
                func.coalesce(func.sum(Order.total), 0).label("total_spent"),
            )
            .outerjoin(Order, Order.user_id == User.id)
            .group_by(User.id)
        )
 
        filters = [
            User.country == country if country else None,
            User.vip == vip if vip is not None else None,
            User.created_at >= created_after if created_after else None,
            User.created_at <= created_before if created_before else None,
            or_(User.name.ilike(f"%{search}%"), User.email.ilike(f"%{search}%")) if search else None
        ]
 
        active_filters = [f for f in filters if f is not None]
        if active_filters:
            stmt = stmt.where(and_(*active_filters))
 
        return stmt
    
    async def get_users(
        self,
        *,
        page: int,
        page_size: int,
        country: str | None = None,
        vip: bool | None = None,
        created_after: datetime | None = None,
        created_before: datetime | None = None,
        search: str | None = None,
        sort: UserSortField = UserSortField.CREATED_AT,
        order: Literal["asc", "desc"] = "desc",
    ) -> tuple[list[tuple[User, int, float]], int]:
        query_params = {k: v for k, v in locals().items() if k in {
            "country", "vip", "created_after", "created_before", "search"
        }}
        stmt = self._base_query(**query_params)
 
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()
 
        sort_column = USER_SORT_COLUMNS.get(sort, User.created_at)
        stmt = stmt.order_by(sort_column.desc() if order == "desc" else sort_column.asc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
 
        result = await self.session.execute(stmt)
        rows = result.all()
        return [(row[0], row[1], float(row[2])) for row in rows], total
    
    async def get_user_with_orders(self, user_id: UUID) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.orders)
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
    
    async def get_user_statistics(self, user_id: UUID):
        stmt = (
            select(
                func.count(Order.id),
                func.coalesce(func.sum(Order.total), 0),
                func.coalesce(func.avg(Order.total), 0),
            )
            .where(Order.user_id == user_id)
        )

        result = await self.session.execute(stmt)

        return result.one()
    
    async def get_distinct_countries(self) -> list[str]:
        stmt = select(User.country).distinct().order_by(User.country)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())