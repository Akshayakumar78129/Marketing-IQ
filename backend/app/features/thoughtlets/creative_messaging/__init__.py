"""
Thoughtlets Creative & Messaging feature module - Creative analytics and insights.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .creative_type_distribution.router import router as creative_type_distribution_router
from .cta_types.router import router as cta_types_router
from .impressions_by_campaign.router import router as impressions_by_campaign_router
from .ctr_by_campaign.router import router as ctr_by_campaign_router
from .ad_set_performance.router import router as ad_set_performance_router
from .creatives.router import router as creatives_router

# Main router for Creative & Messaging feature
router = APIRouter(prefix="/creative-messaging", tags=["Thoughtlets > Creative & Messaging"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(creative_type_distribution_router)
router.include_router(cta_types_router)
router.include_router(impressions_by_campaign_router)
router.include_router(ctr_by_campaign_router)
router.include_router(ad_set_performance_router)
router.include_router(creatives_router)

__all__ = ["router"]
