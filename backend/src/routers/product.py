from uuid import UUID

from fastapi import APIRouter, Depends

from src.dependencies.dependencies import get_product_service
from src.schemes.common import PaginatedResponse
from src.schemes.filters import ProductFilter
from src.schemes.product import (
    ProductDetailResponse,
    ProductTableResponse,
)
from src.schemes.query import (
    Pagination,
    pagination_params,
)
from src.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/", response_model=PaginatedResponse[ProductTableResponse])
async def get_products(pagination: Pagination = Depends(pagination_params), filters: ProductFilter = Depends(), service: ProductService = Depends(get_product_service),):
    return await service.get_products(
        pagination=pagination,
        filters=filters,
    )

@router.get("/categories", response_model=list[str])
async def get_product_categories(service: ProductService = Depends(get_product_service)):
    return await service.get_categories()

@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product(product_id: UUID, service: ProductService = Depends(get_product_service)):
    return await service.get_product(product_id)

