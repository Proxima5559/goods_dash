from decimal import Decimal
from uuid import UUID

from src.schemes.filters import ProductFilter
from src.schemes.query import Pagination
from src.repositories.product_repository import ProductRepository
from src.utils.user_errors import ProductNotFoundException
from src.schemes.common import PaginatedResponse
from src.schemes.product import (
    ProductDetailResponse,
    ProductTableResponse,
)


class ProductService:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_products(
        self,
        pagination: Pagination,
        filters: ProductFilter,
    ) -> PaginatedResponse[ProductTableResponse]:

        products, total = await self.repository.get_products_filtered(
            page=pagination.page,
            page_size=pagination.page_size,
            category=filters.category,
            in_stock=filters.in_stock,
            min_price=filters.min_price,
            max_price=filters.max_price,
            search=filters.search,
            sort=filters.sort.value if hasattr(filters.sort, "value") else filters.sort,
            order=filters.order.value if hasattr(filters.order, "value") else filters.order,
        )

        items = [
            ProductTableResponse.model_validate(product)
            for product in products
        ]

        return PaginatedResponse[ProductTableResponse].build(
            items=items,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total,
        )

    async def get_product(self, product_id: UUID):

        product = await self.repository.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundException(str(product_id))

        orders_count, revenue = await self.repository.get_product_stats(product_id)

        return ProductDetailResponse(
            id=product.id,
            name=product.name,
            category=product.category,
            price=product.price,
            rating=product.rating,
            stock=product.stock,
            remaining_stock=product.stock, 
            orders_count=orders_count,
            revenue_generated=Decimal(revenue) if revenue else Decimal("0.00"),
            average_rating=product.rating
        )
    async def get_categories(self) -> list[str]:
        return await self.repository.get_distinct_categories()