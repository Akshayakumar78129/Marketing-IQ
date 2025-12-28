"""
Meta Ads feature module - Combines all Meta Ads sub-features.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .engagement.router import router as engagement_router
from .campaigns.router import router as campaigns_router
from .daily_performance.router import router as daily_performance_router
from .placements.router import router as placements_router
from .demographics_age.router import router as demographics_age_router
from .demographics_gender.router import router as demographics_gender_router
from .device.router import router as device_router
from .ad_sets.router import router as ad_sets_router
from .ad_creatives.router import router as ad_creatives_router

# Main router for Meta Ads feature
router = APIRouter(prefix="/meta-ads", tags=["Marketing Platforms > Meta Ads"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(engagement_router)
router.include_router(campaigns_router)
router.include_router(daily_performance_router)
router.include_router(placements_router)
router.include_router(demographics_age_router)
router.include_router(demographics_gender_router)
router.include_router(device_router)
router.include_router(ad_sets_router)
router.include_router(ad_creatives_router)

__all__ = ["router"]
