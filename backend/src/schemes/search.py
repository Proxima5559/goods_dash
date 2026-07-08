from uuid import UUID

from pydantic import BaseModel

from .product import ProductResponse
from .user import UserTableResponse


class SearchResponse(BaseModel):
    query: str
    users: list[UserTableResponse]
    products: list[ProductResponse]