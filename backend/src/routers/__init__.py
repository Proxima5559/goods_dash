from fastapi import APIRouter

from .users import router as users_router
from .orders import router as orders_router
from .product import router as products_router
from .dashboard import router as dashboard_router
from .analytics import router as analytics_router


api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(orders_router)
api_router.include_router(products_router)
api_router.include_router(dashboard_router)
api_router.include_router(analytics_router)