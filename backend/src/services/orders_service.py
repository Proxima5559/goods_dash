from uuid import UUID

from src.schemes.filters import OrderFilter
from src.schemes.query import Pagination
from src.utils.user_errors import OrderNotFoundException
from src.repositories.orders_repository import OrderRepository
from src.schemes.common import PaginatedResponse
from src.schemes.order import OrderDetailResponse, OrderListItemResponse


class OrderService:

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def get_orders(
        self,
        pagination: Pagination,
        filters: OrderFilter,
    ) -> PaginatedResponse[OrderListItemResponse]:

        orders, total = await self.repository.get_orders_filtered(
            page=pagination.page,
            page_size=pagination.page_size,
            status=filters.status,
            country=filters.country,
            vip=filters.vip,
            payment=filters.payment,
            date_from=filters.date_from,
            date_to=filters.date_to,
            search=filters.search,
            sort=filters.sort.value,
            order=filters.order.value,
        )

        items = [
            OrderListItemResponse.model_validate(order)
            for order in orders
        ]

        return PaginatedResponse[OrderListItemResponse].build(
            items=items,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total, 
        )

    async def get_order(
        self,
        order_id: UUID,
    ) -> OrderDetailResponse:

        order = await self.repository.get_order_detail(order_id)

        if order is None:
            raise OrderNotFoundException(str(order_id))

        return OrderDetailResponse.model_validate(order)