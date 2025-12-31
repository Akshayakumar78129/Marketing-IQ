"""
Revenue & Lifetime Value - Cohort Retention Pydantic models (DTOs).
"""
from typing import List
from datetime import date
from pydantic import BaseModel, Field


class CohortRetentionItem(BaseModel):
    """Individual cohort retention data for a specific month."""
    cohort_month: date = Field(..., description="Cohort month (first order month)")
    initial_size: int = Field(..., description="Initial cohort size (new customers)")
    months_since: int = Field(..., description="Months since cohort start")
    active_customers: int = Field(..., description="Customers active in this month")
    retention_rate: float = Field(..., description="Retention rate percentage")

    class Config:
        from_attributes = True


class CohortRetentionResponse(BaseModel):
    """Response model for cohort retention table."""
    cohorts: List[CohortRetentionItem] = Field(..., description="List of cohort retention data")
