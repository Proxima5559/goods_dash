from db.database import engine
from models.base import Base

from models.user import User
from models.product import Product
from models.order import Order
from models.order_item import OrderItem


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
