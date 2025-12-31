"""
Thoughtlets Search & Keywords feature module - Keyword performance and search campaign insights.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .top_keywords.router import router as top_keywords_router
from .match_type.router import router as match_type_router
from .keywords.router import router as keywords_router
from .search_campaigns.router import router as search_campaigns_router

# Main router for Search & Keywords feature
router = APIRouter(prefix="/search-keywords", tags=["Thoughtlets > Search & Keywords"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(top_keywords_router)
router.include_router(match_type_router)
router.include_router(keywords_router)
router.include_router(search_campaigns_router)

__all__ = ["router"]
