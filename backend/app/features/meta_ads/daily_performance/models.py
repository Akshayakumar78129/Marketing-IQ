"""
Meta Ads Daily Performance - Pydantic models (DTOs).
"""
from datetime import date as date_type
from typing import List
from pydantic import BaseModel, Field


class MetaAdsDailyPerformanceResponse(BaseModel):
    """Response model for a single day's performance metrics."""
    date: date_type = Field(..., description="Date of the metrics")
    spend: float = Field(..., description="Daily advertising spend")
    impressions: int = Field(..., description="Daily number of impressions")
    clicks: int = Field(..., description="Daily number of clicks")
    conversions: float = Field(..., description="Daily number of conversions")
    revenue: float = Field(..., description="Daily revenue from conversions")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")

    class Config:
        from_attributes = True


class MetaAdsDailyPerformanceListResponse(BaseModel):
    """Response model for list of daily performance metrics."""
    daily_performance: List[MetaAdsDailyPerformanceResponse] = Field(..., description="List of daily metrics")
    total_days: int = Field(..., description="Total number of days")

    class Config:
        from_attributes = True
