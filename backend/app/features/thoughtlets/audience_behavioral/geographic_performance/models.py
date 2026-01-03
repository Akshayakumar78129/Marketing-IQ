"""
Geographic Performance - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class GeoPerformanceItem(BaseModel):
    """Single country with user metrics."""
    country: str = Field(..., description="Country name")
    users: int = Field(..., description="Total users")
    new_users: int = Field(..., description="New users")
    new_user_pct: float = Field(..., description="New user percentage")
    engaged: int = Field(..., description="Number of engaged sessions")
    eng_rate_pct: float = Field(..., description="Engagement rate percentage")

    class Config:
        from_attributes = True


class GeographicPerformanceResponse(BaseModel):
    """Response model for geographic performance metrics."""
    items: list[GeoPerformanceItem] = Field(..., description="List of countries with user metrics")
    total_countries: int = Field(..., description="Total number of countries")

    class Config:
        from_attributes = True
