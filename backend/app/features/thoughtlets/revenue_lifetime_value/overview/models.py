"""
Revenue & Lifetime Value Overview - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class RevenueOverviewResponse(BaseModel):
    """Response model for revenue and lifetime value overview metrics."""
    total_revenue: float = Field(..., description="Total revenue amount")
    avg_clv: float = Field(..., description="Average customer lifetime value")
    historic_clv: float = Field(..., description="Average historic CLV")
    predicted_clv: float = Field(..., description="Average predicted CLV")
    repeat_purchase_rate: float = Field(..., description="Repeat purchase rate percentage")
    clv_cac_ratio: float = Field(..., description="CLV to CAC ratio")
    avg_aov: float = Field(..., description="Average order value")
    churn_risk: float = Field(..., description="Churn risk percentage (High Risk customers)")

    class Config:
        from_attributes = True
