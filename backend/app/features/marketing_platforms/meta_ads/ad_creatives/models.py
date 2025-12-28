"""
Meta Ads Ad Creatives - Pydantic models (DTOs).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class MetaAdsCreativeResponse(BaseModel):
    """Response model for a single ad creative's metrics."""
    ad_id: str = Field(..., description="Unique ad identifier")
    ad_name: str = Field(..., description="Ad creative name")
    ad_type: Optional[str] = Field(None, description="Ad type/format")
    spend: float = Field(..., description="Total advertising spend")
    impressions: int = Field(..., description="Total number of impressions")
    clicks: int = Field(..., description="Total number of clicks")
    conversions: float = Field(..., description="Total number of conversions")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")

    class Config:
        from_attributes = True


class MetaAdsCreativeListResponse(BaseModel):
    """Response model for list of ad creative metrics."""
    creatives: List[MetaAdsCreativeResponse] = Field(..., description="List of ad creative metrics")
    total_count: int = Field(..., description="Total number of creatives")

    class Config:
        from_attributes = True
