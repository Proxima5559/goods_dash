from decimal import Decimal
from uuid import UUID
from datetime import datetime
 
from .common import ORMBase
from .product import ProductResponse
 
 
class OrderUserSummary(ORMBase):
    id: UUID
    name: str
    email: str
    country: str
    vip: bool
 

class OrderBaseResponse(ORMBase):
    id: UUID
    total: Decimal
    status: str
    payment_method: str
    created_at: datetime
    shipped_at: datetime | None
    delivered_at: datetime | None
 
 
class OrderListItemResponse(OrderBaseResponse):
    user: OrderUserSummary
 
 
class OrderItemResponse(ORMBase):
    id: UUID
    quantity: int
    price: Decimal
    product: ProductResponse
 
 
class OrderDetailResponse(OrderBaseResponse):
    user: OrderUserSummary
    items: list[OrderItemResponse]