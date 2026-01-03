"""
Funnel & Attribution thoughtlet module - Funnel and attribution insights.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .ecommerce_funnel.router import router as ecommerce_funnel_router
from .meta_ads_funnel.router import router as meta_ads_funnel_router
from .conversions_by_channel.router import router as conversions_by_channel_router
from .monthly_conversions.router import router as monthly_conversions_router
from .traffic_source_attribution.router import router as traffic_source_attribution_router

# Main router for Funnel & Attribution thoughtlet
router = APIRouter(prefix="/funnel-attribution", tags=["Funnel & Attribution"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(ecommerce_funnel_router)
router.include_router(meta_ads_funnel_router)
router.include_router(conversions_by_channel_router)
router.include_router(monthly_conversions_router)
router.include_router(traffic_source_attribution_router)

__all__ = ["router"]
