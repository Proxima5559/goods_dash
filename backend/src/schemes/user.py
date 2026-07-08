from datetime import datetime
from enum import Enum
from uuid import UUID
from decimal import Decimal

from pydantic import ConfigDict, EmailStr

from .common import ORMBase

class UserSortField(str, Enum):
    NAME = "name"
    EMAIL = "email"
    COUNTRY = "country"
    CREATED_AT = "created_at"
    TOTAL_SPENT = "total_spent"
    ORDERS_COUNT = "orders_count"

class UserResponse(ORMBase):
    id: UUID
    name: str
    email: EmailStr
    city: str
    country: str
    vip: bool
    created_at: datetime

class UserTableResponse(ORMBase):
    id: UUID
    name: str
    email: EmailStr
    country: str
    vip: bool
    created_at: datetime
    orders_count: int
    total_spent: Decimal

class UserOrderSummary(ORMBase):
    id: UUID
    total: Decimal
    status: str
    payment_method: str
    created_at: datetime
    shipped_at: datetime | None
    delivered_at: datetime | None

class UserDetailsResponse(UserResponse):
    orders_count: int
    total_spent: Decimal
    average_order: Decimal
    orders: list[UserOrderSummary]
