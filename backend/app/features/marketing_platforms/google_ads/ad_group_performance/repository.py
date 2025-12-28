"""
Google Ads Ad Group Performance repository - Data access layer for ad group performance metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class AdGroupPerformanceRepository:
    """Repository for Google Ads ad group performance data access operations."""

    @staticmethod
    def get_ad_group_performance(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch Google Ads ad group performance metrics with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with ad group performance metrics
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

        # Build the filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                ag.AD_GROUP_NAME AS "AD_GROUP",
                c.CAMPAIGN_NAME AS "CAMPAIGN",
                SUM(f.IMPRESSIONS) AS "IMPRESSIONS",
                SUM(f.CLICKS) AS "CLICKS",
                ROUND(SUM(f.CLICKS) * 100.0 / NULLIF(SUM(f.IMPRESSIONS), 0), 1) AS "CTR",
                ROUND(SUM(f.SPEND) / NULLIF(SUM(f.CLICKS), 0), 0) AS "CPC",
                ROUND(SUM(f.CONVERSIONS), 0) AS "CONVERSIONS",
                ROUND(SUM(f.CONVERSIONS) * 100.0 / NULLIF(SUM(f.CLICKS), 0), 1) AS "CVR"
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_GROUP_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_AD_GROUP ag
                ON f.AD_GROUP_ID = ag.AD_GROUP_ID
                AND f.PLATFORM = ag.PLATFORM
                AND ag.IS_CURRENT = TRUE
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CAMPAIGN c
                ON f.CAMPAIGN_ID = c.CAMPAIGN_ID
                AND f.PLATFORM = c.PLATFORM
                AND c.IS_CURRENT = TRUE
            WHERE f.PLATFORM = 'google_ads'
                {filter_clause}
            GROUP BY ag.AD_GROUP_NAME, c.CAMPAIGN_NAME
            ORDER BY "IMPRESSIONS" DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ad_group_performance_repository = AdGroupPerformanceRepository()
