from decimal import Decimal

from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_users: int
    vip_users: int

    total_orders: int

    total_revenue: Decimal

    average_order_value: Decimal

    total_products: int

    low_stock_products: int