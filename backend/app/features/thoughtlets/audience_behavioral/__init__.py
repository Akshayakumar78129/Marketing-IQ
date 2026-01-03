"""
Audience & Behavioral thoughtlet - Analytics and behavioral insights.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .engagement_funnel.router import router as engagement_funnel_router
from .traffic_by_source.router import router as traffic_by_source_router
from .users_by_device.router import router as users_by_device_router
from .users_by_country.router import router as users_by_country_router
from .top_pages.router import router as top_pages_router
from .geographic_performance.router import router as geographic_performance_router

# Main router for Audience & Behavioral thoughtlet
router = APIRouter(prefix="/audience-behavioral", tags=["Audience & Behavioral"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(engagement_funnel_router)
router.include_router(traffic_by_source_router)
router.include_router(users_by_device_router)
router.include_router(users_by_country_router)
router.include_router(top_pages_router)
router.include_router(geographic_performance_router)

__all__ = ["router"]
