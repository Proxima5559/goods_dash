from uuid import UUID

from fastapi import APIRouter, Depends

from src.dependencies.dependencies import get_order_service
from src.schemes.common import PaginatedResponse
from src.schemes.filters import (
    OrderFilter,
)
from src.schemes.order import (
    OrderDetailResponse,
    OrderListItemResponse,
)
from src.schemes.query import (
    Pagination,
    pagination_params,
)
from src.services.orders_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get("/",response_model=PaginatedResponse[OrderListItemResponse])

async def get_orders(pagination: Pagination = Depends(pagination_params), filters: OrderFilter = Depends(), service: OrderService = Depends(get_order_service),
):

    return await service.get_orders(
        pagination=pagination,
        filters=filters,
    )


@router.get("/{order_id}",response_model=OrderDetailResponse)
async def get_order(order_id: UUID, service: OrderService = Depends(get_order_service)):

    return await service.get_order(order_id)