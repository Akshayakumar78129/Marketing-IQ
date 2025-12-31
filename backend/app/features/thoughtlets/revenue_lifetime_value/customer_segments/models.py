"""
Revenue & Lifetime Value - Customer Segments Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class CustomerSegmentItem(BaseModel):
    """Individual customer segment item."""
    segment_name: str = Field(..., description="Segment name (New/Minimal, Low Value, Medium Value, High Value)")
    customer_count: int = Field(..., description="Number of customers in this segment")

    class Config:
        from_attributes = True


class CustomerSegmentsResponse(BaseModel):
    """Response model for customer segments distribution."""
    segments: List[CustomerSegmentItem] = Field(..., description="List of customer segments with counts")
