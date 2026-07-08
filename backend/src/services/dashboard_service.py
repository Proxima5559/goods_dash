
from src.repositories.dashboard_repository import DashboardRepository
from src.schemes.dashboard import DashboardResponse


class DashboardService:

    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    async def get_dashboard(self) -> DashboardResponse:

        return DashboardResponse(
            total_users=await self.repository.get_total_users(),
            vip_users=await self.repository.get_vip_users(),
            total_orders=await self.repository.get_total_orders(),
            total_revenue=await self.repository.get_total_revenue(),
            average_order_value=await self.repository.get_average_order(),
            total_products=await self.repository.get_total_products(),
            low_stock_products=await self.repository.get_low_stock_products(),
        )