"""
Users by Country - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class CountryItem(BaseModel):
    """Single country with user count."""
    country: str = Field(..., description="Country name (e.g., 'India', 'United States', '(not set)')")
    users: int = Field(..., description="Number of users from this country")

    class Config:
        from_attributes = True


class UsersByCountryResponse(BaseModel):
    """Response model for users by country geographic distribution."""
    items: list[CountryItem] = Field(..., description="List of countries with user counts")
    total_users: int = Field(..., description="Total users across all countries")

    class Config:
        from_attributes = True
