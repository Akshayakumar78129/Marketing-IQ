"""
Thoughtlets Spend and Budget feature module - Combines all spend and budget sub-features.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .spend_by_platform.router import router as spend_by_platform_router
from .roas_by_platform.router import router as roas_by_platform_router
from .monthly_spend_trend.router import router as monthly_spend_trend_router
from .spend_by_campaign.router import router as spend_by_campaign_router
from .spend_by_ad_group.router import router as spend_by_ad_group_router

# Main router for Spend and Budget feature
router = APIRouter(prefix="/spend-and-budget", tags=["Thoughtlets > Spend and Budget"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(spend_by_platform_router)
router.include_router(roas_by_platform_router)
router.include_router(monthly_spend_trend_router)
router.include_router(spend_by_campaign_router)
router.include_router(spend_by_ad_group_router)

__all__ = ["router"]
