from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from typing import Sequence, TypeVar

T = TypeVar("T")


def weighted_choice(choices: dict[T, float]) -> T:
    items = list(choices.keys())
    weights = list(choices.values())
    return random.choices(items, weights=weights, k=1)[0]


def order_count_for_user() -> int:
    buckets: list[tuple[range, float]] = [
        (range(0, 3), 40),    
        (range(3, 8), 35),    
        (range(8, 15), 18),   
        (range(15, 21), 7),   
    ]
    ranges = [b[0] for b in buckets]
    weights = [b[1] for b in buckets]
    chosen_range = random.choices(ranges, weights=weights, k=1)[0]
    return random.choice(list(chosen_range))


def items_per_order() -> int:
    return random.randint(1, 6)


def quantity_for_item() -> int:
    if random.random() < 0.90:
        return random.randint(1, 3)
    return random.randint(4, 10)

def is_cancelled(rate_min: float = 0.05, rate_max: float = 0.10) -> bool:
    rate = random.uniform(rate_min, rate_max)
    return random.random() < rate


def status_for_age(days_old: int, cancelled: bool) -> str:
 
    if cancelled:
        return "CANCELLED"
    if days_old <= 0:
        return "PENDING"
    if days_old <= 2:
        return "PROCESSING"
    if days_old <= 6:
        return "SHIPPED"
    return "DELIVERED"


def random_datetime_between(start: datetime, end: datetime) -> datetime:
    start = start.replace(tzinfo=None) if start.tzinfo else start
    end = end.replace(tzinfo=None) if end.tzinfo else end
    
    if start >= end:
        return start
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)


def shipping_timeline(ordered_at: datetime, status: str) -> tuple[datetime | None, datetime | None]:

    if status in ("PENDING", "CANCELLED"):
        return None, None

    shipped_at = ordered_at + timedelta(days=random.randint(1, 3))

    if status == "PROCESSING":
        return None, None

    if status == "SHIPPED":
        return shipped_at, None

    delivered_at = shipped_at + timedelta(days=random.randint(2, 6))
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if delivered_at > now:
        delivered_at = now
    if shipped_at > delivered_at:
        shipped_at = delivered_at
    return shipped_at, delivered_at


def pick_in_stock_products(products: Sequence, k: int) -> list:
    available = [p for p in products if p.stock > 0]
    if not available:
        return []
    k = min(k, len(available))
    return random.sample(available, k)