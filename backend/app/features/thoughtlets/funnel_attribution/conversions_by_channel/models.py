"""
Conversions by Channel - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class ChannelConversion(BaseModel):
    """Model for a single channel's conversion metrics."""
    channel: str = Field(..., description="Marketing channel name")
    conversions: int = Field(..., description="Total number of conversions")
    revenue: float = Field(..., description="Total revenue from conversions")

    class Config:
        from_attributes = True


class ConversionsByChannelResponse(BaseModel):
    """Response model for conversions by channel."""
    items: List[ChannelConversion] = Field(..., description="List of channels with conversion metrics")
    total_conversions: int = Field(..., description="Total conversions across all channels")
    total_revenue: float = Field(..., description="Total revenue across all channels")

    class Config:
        from_attributes = True
