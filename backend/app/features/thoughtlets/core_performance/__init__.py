"""
Thoughtlets Core Performance feature module - Combines all core performance sub-features.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .conversions_trend.router import router as conversions_trend_router
from .roas_by_platform.router import router as roas_by_platform_router
from .revenue_vs_spend.router import router as revenue_vs_spend_router

# Main router for Core Performance feature
router = APIRouter(prefix="/core-performance", tags=["Thoughtlets > Core Performance"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(conversions_trend_router)
router.include_router(roas_by_platform_router)
router.include_router(revenue_vs_spend_router)

__all__ = ["router"]
