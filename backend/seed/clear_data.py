from __future__ import annotations
import asyncio

from src.db.session import AsyncSessionLocal  
from sqlalchemy import delete
from src.models import User, Product, Order, OrderItem

async def run() -> None:
    session = AsyncSessionLocal()
    try:
        print("Clearing old seed data...")
        await session.execute(delete(OrderItem)) 
        await session.execute(delete(Order))
        await session.execute(delete(Product))
        await session.execute(delete(User))
        await session.flush()
        
        await session.commit()
        print("Done: Data cleared from all tables.")
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(run())
