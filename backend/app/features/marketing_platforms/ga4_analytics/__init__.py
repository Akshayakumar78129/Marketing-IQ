"""
GA4 Analytics feature module - Combines all GA4 Analytics sub-features.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .traffic_sources.router import router as traffic_sources_router
from .daily_traffic_trend.router import router as daily_traffic_trend_router
from .hourly_traffic_pattern.router import router as hourly_traffic_pattern_router
from .conversion_funnel.router import router as conversion_funnel_router
from .technology_breakdown.router import router as technology_breakdown_router
from .top_pages.router import router as top_pages_router
from .landing_pages.router import router as landing_pages_router
from .geographic_performance.router import router as geographic_performance_router

# Main router for GA4 Analytics feature
router = APIRouter(prefix="/ga4-analytics", tags=["Marketing Platforms > GA4 Analytics"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(traffic_sources_router)
router.include_router(daily_traffic_trend_router)
router.include_router(hourly_traffic_pattern_router)
router.include_router(conversion_funnel_router)
router.include_router(technology_breakdown_router)
router.include_router(top_pages_router)
router.include_router(landing_pages_router)
router.include_router(geographic_performance_router)

__all__ = ["router"]
