from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.dashboard_repository import DashboardRepository
from src.repositories.orders_repository import OrderRepository
from src.services.orders_service import OrderService

from src.repositories.user_repository import UserRepository
from src.services.dashboard_service import DashboardService
from src.repositories.product_repository import ProductRepository
from src.services.product_service import ProductService
# from src.services.search_service import SearchService
from src.services.user_service import UserService
from src.db.session import get_db  
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.repositories.analytics_repository import AnalyticsRepository
from src.services.analytics_service import AnalyticsService

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)

def get_dashboard_service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    dashboard_repository = DashboardRepository(db)
    return DashboardService(dashboard_repository)

def get_order_repository(db: AsyncSession = Depends(get_db),) -> OrderRepository:
    return OrderRepository(db)


def get_order_service(repository: OrderRepository = Depends(get_order_repository),) -> OrderService:
    return OrderService(repository)

def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(repository: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository)

def get_analytics_repository(db: AsyncSession = Depends(get_db)) -> AnalyticsRepository:
    return AnalyticsRepository(db)


def get_analytics_service(
    repository: AnalyticsRepository = Depends(get_analytics_repository),
) -> AnalyticsService:
    return AnalyticsService(repository)