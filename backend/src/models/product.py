from __future__ import annotations
from uuid import UUID, uuid4

from sqlalchemy import Float, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .order_item import OrderItem
from .base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    name: Mapped[str] = mapped_column(String(150))
    category: Mapped[str] = mapped_column(String(100))

    price: Mapped[float] = mapped_column(Numeric(10, 2))

    rating: Mapped[float] = mapped_column(Float)

    stock: Mapped[int] = mapped_column(Integer)

    order_items: Mapped[list[OrderItem]] = relationship(
        back_populates="product"
    )