"""
Google Ads feature module - Combines all Google Ads sub-features.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .campaign_performance.router import router as campaign_performance_router
from .spend_by_campaign_type.router import router as spend_by_campaign_type_router
from .daily_performance_trend.router import router as daily_performance_trend_router
from .account_health.router import router as account_health_router
from .ad_group_performance.router import router as ad_group_performance_router
from .keyword_performance.router import router as keyword_performance_router
from .top_keywords.router import router as top_keywords_router

# Main router for Google Ads feature
router = APIRouter(prefix="/google-ads", tags=["Marketing Platforms > Google Ads"])

# Include all feature routers
router.include_router(overview_router)
router.include_router(campaign_performance_router)
router.include_router(spend_by_campaign_type_router)
router.include_router(daily_performance_trend_router)
router.include_router(account_health_router)
router.include_router(ad_group_performance_router)
router.include_router(keyword_performance_router)
router.include_router(top_keywords_router)

__all__ = ["router"]
