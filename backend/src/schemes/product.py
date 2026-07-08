from uuid import UUID

from decimal import Decimal

from .common import ORMBase

class ProductResponse(ORMBase):
    id: UUID
    name: str
    category: str
    price: Decimal
    rating: Decimal
    stock: int

class ProductTableResponse(ProductResponse):
    pass

class ProductDetailResponse(ProductResponse):
    orders_count: int
    revenue_generated: Decimal
    average_rating: Decimal
    remaining_stock: int
 