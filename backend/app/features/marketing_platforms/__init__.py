"""
Marketing Platforms feature module - Combines all marketing platform sub-features.
"""
from fastapi import APIRouter

from .google_ads import router as google_ads_router
from .meta_ads import router as meta_ads_router
from .ga4_analytics import router as ga4_analytics_router

# Main router for Marketing Platforms feature
router = APIRouter(prefix="/marketing-platforms")

# Include all platform routers
router.include_router(google_ads_router)
router.include_router(meta_ads_router)
router.include_router(ga4_analytics_router)

__all__ = ["router"]
