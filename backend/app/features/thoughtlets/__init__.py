"""
Thoughtlets feature module - Aggregated insights across all platforms.
"""
from fastapi import APIRouter

from .core_performance import router as core_performance_router
from .search_keywords import router as search_keywords_router
from .revenue_lifetime_value import router as revenue_lifetime_value_router

# Main router for Thoughtlets feature
router = APIRouter(prefix="/thoughtlets")

# Include all sub-feature routers
router.include_router(core_performance_router)
router.include_router(search_keywords_router)
router.include_router(revenue_lifetime_value_router)

__all__ = ["router"]
