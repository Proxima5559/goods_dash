from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from src.models.order import OrderStatus, PaymentMethod


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"



class UserSortField(str, Enum):
    NAME = "name"
    EMAIL = "email"
    COUNTRY = "country"
    CREATED_AT = "created_at"
    ORDERS_COUNT = "orders_count"
    TOTAL_SPENT = "total_spent"


class UserFilter(BaseModel):
    country: str | None = None
    vip: bool | None = None

    created_after: datetime | None = None
    created_before: datetime | None = None

    search: str | None = None

    sort: UserSortField = UserSortField.CREATED_AT
    order: SortDirection = SortDirection.DESC



class OrderSortField(str, Enum):
    CREATED_AT = "created_at"
    TOTAL = "total"
    STATUS = "status"
    SHIPPED_AT = "shipped_at"
    DELIVERED_AT = "delivered_at"


class OrderFilter(BaseModel):
    status: OrderStatus | None = None

    country: str | None = None

    vip: bool | None = None

    payment: PaymentMethod | None = None

    date_from: datetime | None = None
    date_to: datetime | None = None

    search: str | None = None

    sort: OrderSortField = OrderSortField.CREATED_AT
    order: SortDirection = SortDirection.DESC



class ProductSortField(str, Enum):
    NAME = "name"
    CATEGORY = "category"
    PRICE = "price"
    RATING = "rating"
    STOCK = "stock"


class ProductFilter(BaseModel):
    category: str | None = None

    in_stock: bool | None = None

    min_price: float | None = None
    max_price: float | None = None

    search: str | None = None

    sort: ProductSortField = ProductSortField.NAME
    order: SortDirection = SortDirection.ASC