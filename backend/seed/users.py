from __future__ import annotations

import random
from datetime import datetime, timezone

from faker import Faker

from src.models.user import User
from .consonats import COUNTRIES, VIP_RATE, _FAKERS


def generate_users(n: int, start_date: str = "-2y") -> list[User]:
    users: list[User] = []

    for _ in range(n):
        country, locale = random.choice(list(COUNTRIES.items()))
        fake = _FAKERS[locale]

        first_name = fake.first_name()
        last_name = fake.last_name()
        name = f"{first_name} {last_name}"

     
        email = fake.unique.email()

        city = fake.city()
        vip = random.random() < VIP_RATE

        created_at = fake.date_time_between(
            start_date=start_date, end_date="now", tzinfo=timezone.utc
        )

        users.append(
            User(
                name=name,
                email=email,
                city=city,
                country=country,
                vip=vip,
                created_at=created_at,
            )
        )

    return users