"""
Meta Ads Engagement repository - Data access layer for engagement metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class MetaAdsEngagementRepository:
    """Repository for Meta Ads engagement data access operations."""

    @staticmethod
    def get_engagement_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Optional[dict]:
        """
        Fetch aggregated Meta Ads engagement metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated metrics or None if no data
        """
        # Build date filter conditions
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                COALESCE(SUM(LINK_CLICKS), 0) AS TOTAL_LINK_CLICKS,
                COALESCE(SUM(POST_ENGAGEMENTS), 0) AS TOTAL_POST_ENGAGEMENTS,
                COALESCE(SUM(PAGE_ENGAGEMENTS), 0) AS TOTAL_PAGE_ENGAGEMENTS,
                COALESCE(SUM(POST_REACTIONS), 0) AS TOTAL_POST_REACTIONS,
                COALESCE(SUM(VIEW_CONTENT), 0) AS TOTAL_VIEW_CONTENT,
                COALESCE(SUM(ADD_TO_CART), 0) AS TOTAL_ADD_TO_CART,
                COALESCE(SUM(INITIATE_CHECKOUT), 0) AS TOTAL_INITIATE_CHECKOUT,
                COALESCE(SUM(PURCHASES), 0) AS TOTAL_PURCHASES,
                COALESCE(SUM(TOTAL_ACTIONS), 0) AS TOTAL_ACTIONS,
                COALESCE(AVG(VIEW_TO_CART_RATE), 0) AS AVG_VIEW_TO_CART_RATE,
                COALESCE(AVG(CART_TO_CHECKOUT_RATE), 0) AS AVG_CART_TO_CHECKOUT_RATE,
                COALESCE(AVG(CHECKOUT_TO_PURCHASE_RATE), 0) AS AVG_CHECKOUT_TO_PURCHASE_RATE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_META_CONVERSION
            WHERE PLATFORM = 'meta'
                {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else None


# Singleton instance for dependency injection
meta_ads_engagement_repository = MetaAdsEngagementRepository()
