"""
Revenue & Lifetime Value - Retention Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class RetentionResponse(BaseModel):
    """Response model for retention metrics by period."""
    retention_30d: float = Field(..., description="30-day retention rate percentage")
    retention_60d: float = Field(..., description="60-day retention rate percentage")
    retention_90d: float = Field(..., description="90-day retention rate percentage")
    retained_30d_count: int = Field(..., description="Number of customers retained after 30 days")
    retained_60d_count: int = Field(..., description="Number of customers retained after 60 days")
    retained_90d_count: int = Field(..., description="Number of customers retained after 90 days")

    class Config:
        from_attributes = True
