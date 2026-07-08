from __future__ import annotations

from datetime import datetime, timezone

from .consonats import PAYMENT_WEIGHTS, STATUS_MAP
from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.product import Product
from src.models.user import User

from .utils import (
    is_cancelled,
    items_per_order,
    order_count_for_user,
    pick_in_stock_products,
    quantity_for_item,
    random_datetime_between,
    shipping_timeline,
    status_for_age,
    weighted_choice,
)


def _build_single_order(user: User, products: list[Product], now: datetime) -> Order | None:
    chosen_products = pick_in_stock_products(products, items_per_order())
    if not chosen_products:
        return None

    created_at = random_datetime_between(user.created_at, now)
    days_old = (now - created_at).days

    cancelled = is_cancelled()
    status_str = status_for_age(days_old, cancelled)
    status = STATUS_MAP[status_str]

    payment_method = weighted_choice(PAYMENT_WEIGHTS)

    shipped_at, delivered_at = shipping_timeline(created_at, status_str)

    order = Order(
        user_id=user.id,
        status=status,
        payment_method=payment_method,
        created_at=created_at,
        shipped_at=shipped_at,
        delivered_at=delivered_at,
        total=0,  
    )

    total = 0
    items: list[OrderItem] = []
    for product in chosen_products:
        max_qty = min(quantity_for_item(), product.stock)
        if max_qty <= 0:
            continue

        line_total = product.price * max_qty
        total += line_total

        items.append(
            OrderItem(
                product_id=product.id,
                quantity=max_qty,
                price=product.price,  
            )
        )

     
        product.stock -= max_qty

    if not items:
        return None

    order.total = total
    order.items = items

    return order


def generate_orders(users: list[User], products: list[Product]) -> list[Order]:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    orders: list[Order] = []

    for user in users:
        n_orders = order_count_for_user()
        for _ in range(n_orders):
            order = _build_single_order(user, products, now)
            if order is None:
                break
            orders.append(order)

    return orders