from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from src.models.order_item import OrderItem
from src.models.product import Product
from src.schemes.filters import ProductSortField

PRODUCT_SORT_COLUMNS = {
    ProductSortField.NAME: Product.name,
    ProductSortField.CATEGORY: Product.category,
    ProductSortField.PRICE: Product.price,
    ProductSortField.RATING: Product.rating,
    ProductSortField.STOCK: Product.stock,
}


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Product, session=session)

    def _filtered_query(
        self,
        *,
        category: str | None = None,
        in_stock: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        search: str | None = None,
    ):
        stmt = select(Product)

        filters = [
            Product.category == category if category else None,
            (Product.stock > 0 if in_stock else Product.stock <= 0) if in_stock is not None else None,
            Product.price >= min_price if min_price is not None else None,
            Product.price <= max_price if max_price is not None else None,
            Product.name.ilike(f"%{search}%") if search else None
        ]

        active_filters = [f for f in filters if f is not None]
        if active_filters:
            stmt = stmt.where(and_(*active_filters))

        return stmt

    async def get_products_filtered(
        self,
        *,
        page: int,
        page_size: int,
        category: str | None = None,
        in_stock: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        search: str | None = None,
        sort: str = "name",
        order: str = "asc",
    ) -> tuple[list[Product], int]:
        
        filter_keys = {"category", "in_stock", "min_price", "max_price", "search"}
        query_params = {k: v for k, v in locals().items() if k in filter_keys}
        
        base_stmt = self._filtered_query(**query_params)

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        sort_column = PRODUCT_SORT_COLUMNS.get(sort, Product.name)
        stmt = (
            base_stmt.order_by(sort_column.desc() if order == "desc" else sort_column.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_product_stats(self, product_id: UUID):
        stmt = (
            select(
                func.count(OrderItem.id),
                func.coalesce(func.sum(OrderItem.price * OrderItem.quantity), 0),
            )
            .where(OrderItem.product_id == product_id)
        )
        result = await self.session.execute(stmt)
        return result.one()