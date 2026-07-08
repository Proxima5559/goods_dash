from fastapi import APIRouter, Depends
from src.schemes.dashboard import DashboardResponse
from src.services.dashboard_service import DashboardService
from src.dependencies.dependencies import get_dashboard_service

router = APIRouter(prefix="/dashboard",tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
async def get_dashboard(service: DashboardService = Depends(get_dashboard_service)):
    return await service.get_dashboard()