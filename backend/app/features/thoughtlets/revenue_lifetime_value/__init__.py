"""
Thoughtlets Revenue & Lifetime Value feature module - Customer analytics and CLV insights.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
from .clv_breakdown.router import router as clv_breakdown_router
from .customer_segments.router import router as customer_segments_router
from .churn_distribution.router import router as churn_distribution_router
from .customer_types.router import router as customer_types_router
from .retention.router import router as retention_router
from .cac_metrics.router import router as cac_metrics_router
from .cohort_retention.router import router as cohort_retention_router

# Main router for Revenue & Lifetime Value feature
router = APIRouter(prefix="/revenue-lifetime-value", tags=["Thoughtlets > Revenue & Lifetime Value"])

# Include all sub-feature routers
router.include_router(overview_router)
router.include_router(clv_breakdown_router)
router.include_router(customer_segments_router)
router.include_router(churn_distribution_router)
router.include_router(customer_types_router)
router.include_router(retention_router)
router.include_router(cac_metrics_router)
router.include_router(cohort_retention_router)

__all__ = ["router"]
