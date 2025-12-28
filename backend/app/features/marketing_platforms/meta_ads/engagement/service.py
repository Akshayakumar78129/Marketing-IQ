"""
Meta Ads Engagement service - Business logic layer for engagement operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import meta_ads_engagement_repository
from .models import MetaAdsEngagementResponse


class MetaAdsEngagementService:
    """Service class for Meta Ads engagement business logic."""

    def __init__(self, repository=meta_ads_engagement_repository):
        self.repository = repository

    def get_engagement(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> MetaAdsEngagementResponse:
        """
        Get Meta Ads engagement metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            MetaAdsEngagementResponse with aggregated metrics

        Raises:
            HTTPException: 400 if date_from > date_to
            HTTPException: 404 if no data found
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch metrics from repository
        metrics = self.repository.get_engagement_metrics(date_from, date_to)

        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Meta Ads engagement data found for date range {date_from} to {date_to}"
            )

        # Map database result (uppercase keys from Snowflake) to response model
        return self._map_to_response(metrics)

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsEngagementResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsEngagementResponse(
            link_clicks=int(data.get("TOTAL_LINK_CLICKS") or 0),
            post_engagements=int(data.get("TOTAL_POST_ENGAGEMENTS") or 0),
            page_engagements=int(data.get("TOTAL_PAGE_ENGAGEMENTS") or 0),
            post_reactions=int(data.get("TOTAL_POST_REACTIONS") or 0),
            view_content=int(data.get("TOTAL_VIEW_CONTENT") or 0),
            add_to_cart=int(data.get("TOTAL_ADD_TO_CART") or 0),
            initiate_checkout=int(data.get("TOTAL_INITIATE_CHECKOUT") or 0),
            purchases=int(data.get("TOTAL_PURCHASES") or 0),
            total_actions=int(data.get("TOTAL_ACTIONS") or 0),
            view_to_cart_rate=float(data.get("AVG_VIEW_TO_CART_RATE") or 0),
            cart_to_checkout_rate=float(data.get("AVG_CART_TO_CHECKOUT_RATE") or 0),
            checkout_to_purchase_rate=float(data.get("AVG_CHECKOUT_TO_PURCHASE_RATE") or 0)
        )


# Singleton instance for dependency injection
meta_ads_engagement_service = MetaAdsEngagementService()
