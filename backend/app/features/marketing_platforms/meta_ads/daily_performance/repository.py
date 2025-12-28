"""
Meta Ads Daily Performance repository - Data access layer for daily metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class MetaAdsDailyPerformanceRepository:
    """Repository for Meta Ads daily performance data access operations."""

    @staticmethod
    def get_daily_performance(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        campaign_id: Optional[str] = None
    ) -> List[dict]:
        """
        Fetch Meta Ads daily performance metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            campaign_id: Optional campaign ID filter

        Returns:
            List of dictionaries with daily metrics
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

        if campaign_id:
            conditions.append("CAMPAIGN_ID = %(campaign_id)s")
            params["campaign_id"] = campaign_id

        # Build filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                DATE_DAY,
                SUM(SPEND) AS DAILY_SPEND,
                SUM(IMPRESSIONS) AS DAILY_IMPRESSIONS,
                SUM(CLICKS) AS DAILY_CLICKS,
                COALESCE(SUM(CONVERSIONS), 0) AS DAILY_CONVERSIONS,
                COALESCE(SUM(CONVERSION_VALUE), 0) AS DAILY_REVENUE,
                CASE WHEN SUM(IMPRESSIONS) > 0 THEN (SUM(CLICKS) / SUM(IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                CASE WHEN SUM(CLICKS) > 0 THEN SUM(SPEND) / SUM(CLICKS) ELSE 0 END AS CPC
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            WHERE PLATFORM = 'meta'
                {filter_clause}
            GROUP BY DATE_DAY
            ORDER BY DATE_DAY ASC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
meta_ads_daily_performance_repository = MetaAdsDailyPerformanceRepository()
