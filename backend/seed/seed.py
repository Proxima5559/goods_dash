from __future__ import annotations
import asyncio

from src.db.session import AsyncSessionLocal  
from sqlalchemy import delete
from src.models import User, Product, Order, OrderItem
from .orders import generate_orders
from .products import generate_products
from .users import generate_users
 
NUM_USERS = 200
 
 
async def run(num_users: int = NUM_USERS) -> None:
    session = AsyncSessionLocal()
    try:
        print("Clearing old seed data...")
        await session.execute(delete(OrderItem)) 
        await session.execute(delete(Order))
        await session.execute(delete(Product))
        await session.execute(delete(User))
        await session.flush()

        print("Seeding products...")
        products = generate_products()
        session.add_all(products)
        await session.flush()  
 
        print(f"Seeding {num_users} users...")
        users = generate_users(num_users)
        session.add_all(users)
        await session.flush() 
 
        print("Seeding orders...")
        orders = generate_orders(users, products)
        session.add_all(orders)
 
        await session.commit()
        print(
            f"Done: {len(products)} products, {len(users)} users, "
            f"{len(orders)} orders."
        )
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
 
 
if __name__ == "__main__":
    asyncio.run(run())