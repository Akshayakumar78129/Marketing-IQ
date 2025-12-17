"""
Google Ads Campaign Performance repository - Data access layer for campaign performance metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class CampaignPerformanceRepository:
    """Repository for Google Ads campaign performance data access operations."""

    @staticmethod
    def get_campaign_performance(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status: Optional[str] = None
    ) -> list[dict]:
        """
        Fetch Google Ads campaign performance metrics with optional filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            status: Optional campaign status filter (e.g., 'Active', 'Paused')

        Returns:
            List of dictionaries with campaign performance metrics
        """
        # Build filter conditions
        conditions = []
        params = {}

        if date_from:
            conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        if status:
            conditions.append("c.STATUS = %(status)s")
            params["status"] = status

        # Build the filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                c.CAMPAIGN_NAME AS "CAMPAIGN",
                c.STATUS AS "STATUS",
                ROUND(SUM(f.SPEND), 0) AS "SPEND",
                ROUND(SUM(f.CONVERSION_VALUE), 0) AS "REVENUE",
                ROUND(SUM(f.CONVERSION_VALUE) / NULLIF(SUM(f.SPEND), 0), 1) AS "ROAS",
                ROUND(SUM(f.CONVERSIONS)) AS "CONVERSIONS",
                ROUND(SUM(f.CLICKS) * 100.0 / NULLIF(SUM(f.IMPRESSIONS), 0), 1) AS "CTR",
                ROUND(SUM(f.SPEND) / NULLIF(SUM(f.CLICKS), 0)) AS "CPC"
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CAMPAIGN c
                ON f.CAMPAIGN_ID = c.CAMPAIGN_ID
                AND f.PLATFORM = c.PLATFORM
                AND c.IS_CURRENT = TRUE
            WHERE f.PLATFORM = 'google_ads'
                {filter_clause}
            GROUP BY c.CAMPAIGN_NAME, c.STATUS
            ORDER BY "SPEND" DESC
        """
        print(query)

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
campaign_performance_repository = CampaignPerformanceRepository()
