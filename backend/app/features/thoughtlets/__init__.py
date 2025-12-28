"""
Thoughtlets feature module - Aggregated insights across all platforms.
"""
from fastapi import APIRouter

from .core_performance import router as core_performance_router

# Main router for Thoughtlets feature
router = APIRouter(prefix="/thoughtlets")

# Include all sub-feature routers
router.include_router(core_performance_router)

__all__ = ["router"]
