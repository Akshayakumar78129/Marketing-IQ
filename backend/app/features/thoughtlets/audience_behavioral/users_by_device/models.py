"""
Users by Device Type - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class DeviceTypeItem(BaseModel):
    """Single device type with user count."""
    device_type: str = Field(..., description="Device category (e.g., 'desktop', 'mobile', 'Unknown')")
    users: int = Field(..., description="Number of users for this device type")

    class Config:
        from_attributes = True


class UsersByDeviceResponse(BaseModel):
    """Response model for users by device type breakdown."""
    items: list[DeviceTypeItem] = Field(..., description="List of device types with user counts")
    total_users: int = Field(..., description="Total users across all device types")

    class Config:
        from_attributes = True
