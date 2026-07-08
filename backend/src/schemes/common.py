from uuid import UUID
from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UUIDResponse(ORMBase):
    id: UUID

class PageMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
 
 
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    meta: PageMeta
 
    @classmethod
    def build(cls, items: list[T], page: int, page_size: int, total_items: int) -> "PaginatedResponse[T]":
        total_pages = (total_items + page_size - 1) // page_size if page_size else 0
        return cls(
            items=items,
            meta=PageMeta(
                page=page,
                page_size=page_size,
                total_items=total_items,
                total_pages=total_pages,
            ),
        )
 