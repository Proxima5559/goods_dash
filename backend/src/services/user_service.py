from datetime import datetime
from decimal import Decimal

from src.schemes.common import PaginatedResponse
from src.schemes.filters import SortDirection
from src.schemes.user import UserDetailsResponse, UserSortField, UserTableResponse
from src.repositories.user_repository import UserRepository
from src.models.user import User
from typing import List
from uuid import UUID
from src.utils.user_errors import UserNotFoundException
from src.core.constants import to_money 
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

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
        order: SortDirection = SortDirection.DESC,
    ) -> PaginatedResponse[UserTableResponse]:

        rows, total = await self.user_repository.get_users(
            page=page,
            page_size=page_size,
            country=country,
            vip=vip,
            created_after=created_after,
            created_before=created_before,
            search=search,
            sort=sort.value if hasattr(sort, "value") else sort,
            order=order,
        )

        users = [
            UserTableResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                country=user.country,
                vip=user.vip,
                created_at=user.created_at,
                orders_count=orders_count,
                total_spent=to_money(total_spent),
            )
            for user, orders_count, total_spent in rows
        ]

        return PaginatedResponse.build(
            items=users,
            page=page,
            page_size=page_size,
            total_items=total,
        )
    
    async def get_user(self, user_id: UUID) -> UserDetailsResponse:

        user = await self.user_repository.get_user_with_orders(user_id)

        if user is None:
            raise UserNotFoundException(str(user_id))

        count, total, average = (
            await self.user_repository.get_user_statistics(user_id)
        )

        return UserDetailsResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            city=user.city,
            country=user.country,
            vip=user.vip,
            created_at=user.created_at,
            orders_count=count,
            total_spent=to_money(total),
            average_order=to_money(average),
            orders=user.orders,
        )
    async def get_countries(self) -> list[str]:
        return await self.user_repository.get_distinct_countries()