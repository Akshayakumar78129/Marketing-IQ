"""
Revenue & Lifetime Value - Customer Types Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class CustomerTypesResponse(BaseModel):
    """Response model for customer type distribution."""
    new_customers: int = Field(..., description="Number of new customers")
    repeat_customers: int = Field(..., description="Number of repeat customers")
    one_time_customers: int = Field(..., description="Number of one-time customers")

    class Config:
        from_attributes = True
