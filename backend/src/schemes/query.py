from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    page_size: int

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


def pagination_params(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> Pagination:
    return Pagination(
        page=page,
        page_size=page_size,
    )