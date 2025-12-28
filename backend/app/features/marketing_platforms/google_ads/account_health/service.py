"""
Google Ads Account Health service - Business logic layer for account health operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import account_health_repository
from .models import AccountHealthResponse


class AccountHealthService:
    """Service class for Google Ads account health business logic."""

    def __init__(self, repository=account_health_repository):
        self.repository = repository

    def get_account_health(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> AccountHealthResponse:
        """
        Get Google Ads account health metrics with optional date filters for ROAS.

        Args:
            date_from: Optional start date for ROAS calculation
            date_to: Optional end date for ROAS calculation

        Returns:
            AccountHealthResponse with account health metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch metrics from repository
        data = self.repository.get_account_health(
            date_from=date_from,
            date_to=date_to
        )

        # Map database result to response model
        return AccountHealthResponse(
            total_campaigns=int(data.get("TOTAL_CAMPAIGNS") or 0),
            active_campaigns=int(data.get("ACTIVE_CAMPAIGNS") or 0),
            avg_roas=float(data.get("AVG_ROAS")) if data.get("AVG_ROAS") is not None else None,
            total_keywords=int(data.get("TOTAL_KEYWORDS") or 0)
        )


# Singleton instance for dependency injection
account_health_service = AccountHealthService()
