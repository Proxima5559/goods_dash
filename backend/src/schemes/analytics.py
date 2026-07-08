from decimal import Decimal

from pydantic import BaseModel


class MonthlyRevenuePoint(BaseModel):
    month: str 
    revenue: Decimal


class OrderStatusCount(BaseModel):
    status: str
    count: int


class OrderCountryCount(BaseModel):
    country: str
    orders: int


class MonthlyUserCount(BaseModel):
    month: str 
    users: int


class TopProductItem(BaseModel):
    id: str
    name: str
    category: str
    orders_count: int
    units_sold: int
    revenue: Decimal


class CategorySales(BaseModel):
    category: str
    revenue: Decimal
    units_sold: int


class PaymentMethodStats(BaseModel):
    payment_method: str
    count: int
    revenue: Decimal


class HeatmapCell(BaseModel):
    weekday: int 
    hour: int  
    revenue: Decimal
    orders_count: int
