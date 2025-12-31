"""
Revenue & Lifetime Value - CAC Metrics Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class CACMetricsResponse(BaseModel):
    """Response model for Customer Acquisition Cost metrics."""
    cac_google: float = Field(..., description="Customer Acquisition Cost for Google Ads")
    cac_meta: float = Field(..., description="Customer Acquisition Cost for Meta Ads")
    cac_blended: float = Field(..., description="Blended Customer Acquisition Cost")
    google_ads_spend: float = Field(..., description="Total Google Ads spend")
    meta_ads_spend: float = Field(..., description="Total Meta Ads spend")
    total_ad_spend: float = Field(..., description="Total advertising spend")

    class Config:
        from_attributes = True
