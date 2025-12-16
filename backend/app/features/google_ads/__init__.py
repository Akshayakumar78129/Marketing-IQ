"""
Google Ads feature module - Combines all Google Ads sub-features.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router

# Main router for Google Ads feature
router = APIRouter(prefix="/google-ads", tags=["Google Ads"])

# Include all feature routers
router.include_router(overview_router)

__all__ = ["router"]
