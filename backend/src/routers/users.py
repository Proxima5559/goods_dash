import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemes.query import Pagination, pagination_params
from src.schemes.common import PaginatedResponse
from src.schemes.user import UserDetailsResponse, UserSortField, UserTableResponse
from src.services.user_service import UserService
from src.dependencies.dependencies import get_user_service
from src.schemes.user import UserResponse
from typing import Literal

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=PaginatedResponse[UserTableResponse])
async def get_users(
    pagination: Pagination = Depends(pagination_params),
    country: str | None = Query(None, description="Exact country match"),
    vip: bool | None = Query(None, description="Filter by VIP status"),
    created_after: datetime.datetime | None = Query(None, description="Users created on/after this date"),
    created_before: datetime.datetime | None = Query(None, description="Users created on/before this date"),
    search: str | None = Query(None, description="Search by name or email"),
    sort: UserSortField = Query("created_at"),
    order: Literal["asc", "desc"] = Query("desc"),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_users(
        page=pagination.page,
        page_size=pagination.page_size,
        country=country,
        vip=vip,
        created_after=created_after,
        created_before=created_before,
        search=search,
        sort=sort,
        order=order,
    )

@router.get("/{user_id}", response_model=UserDetailsResponse)
async def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    return await user_service.get_user(user_id)