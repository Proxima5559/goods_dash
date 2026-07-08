from __future__ import annotations
import random

from faker import Faker
import faker_commerce

from src.models.product import Product
from .consonats import CATEGORY_CONFIG

fake = Faker()
fake.add_provider(faker_commerce.Provider)


def generate_products(n: int = 60) -> list[Product]:
    products: list[Product] = []
    categories = list(CATEGORY_CONFIG.keys())
    for _ in range(n):
        category = random.choice(categories)
        config = CATEGORY_CONFIG[category]
        base_name = random.choice(config["items"])
        name = f"{fake.word().capitalize()} {base_name}"
        min_p, max_p = config["price_range"]
        price = fake.pydecimal(left_digits=4, right_digits=2, min_value=min_p, max_value=max_p)
        rating = round(fake.pyfloat(min_value=3.0, max_value=5.0), 1)
        

        products.append(
            Product(
                name=name,
                category=category,
                price=price,
                rating=rating,
                stock=random.choice([0, 10, 50, 200, random.randint(1, 200)])
            )
        )

    return products