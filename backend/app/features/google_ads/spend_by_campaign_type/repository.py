"""
Google Ads Spend by Campaign Type repository - Data access layer for spend breakdown by campaign type.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class SpendByCampaignTypeRepository:
    """Repository for Google Ads spend by campaign type data access operations."""

    @staticmethod
    def get_spend_by_campaign_type(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch Google Ads spend breakdown by campaign type with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with campaign type spend breakdown
        """
        # Build filter conditions
        conditions = []
        params = {}

        if date_from:
            conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        # Build the filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                CASE CAMPAIGN_TYPE
                    WHEN 'PERFORMANCE_MAX' THEN 'Performance Max'
                    WHEN 'SEARCH' THEN 'Search'
                    WHEN 'SHOPPING' THEN 'Shopping'
                    WHEN 'VIDEO' THEN 'Video'
                    WHEN 'DEMAND_GEN' THEN 'Demand Gen'
                    WHEN 'DISPLAY' THEN 'Display'
                    ELSE INITCAP(REPLACE(CAMPAIGN_TYPE, '_', ' '))
                END AS "CAMPAIGN_TYPE",
                SUM(SPEND) AS "TOTAL_SPEND",
                SUM(SPEND) * 100.0 / SUM(SUM(SPEND)) OVER() AS "SPEND_PERCENTAGE"
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            WHERE PLATFORM = 'google_ads'
                {filter_clause}
            GROUP BY CAMPAIGN_TYPE
            ORDER BY "TOTAL_SPEND" DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
spend_by_campaign_type_repository = SpendByCampaignTypeRepository()
