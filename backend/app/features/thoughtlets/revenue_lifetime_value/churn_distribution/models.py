"""
Revenue & Lifetime Value - Churn Distribution Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class ChurnDistributionItem(BaseModel):
    """Individual churn risk distribution item."""
    risk_level: str = Field(..., description="Risk level (Low Risk, Healthy, Medium Risk, High Risk)")
    customer_count: int = Field(..., description="Number of customers in this risk level")

    class Config:
        from_attributes = True


class ChurnDistributionResponse(BaseModel):
    """Response model for churn risk distribution."""
    distribution: List[ChurnDistributionItem] = Field(..., description="List of churn risk distribution by level")
