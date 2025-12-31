"""
Revenue & Lifetime Value - CLV Breakdown Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class CLVBreakdownResponse(BaseModel):
    """Response model for CLV breakdown (overall averages)."""
    historic_clv: float = Field(..., description="Average historic CLV")
    predicted_clv: float = Field(..., description="Average predicted CLV")
    total_clv: float = Field(..., description="Average total CLV")
