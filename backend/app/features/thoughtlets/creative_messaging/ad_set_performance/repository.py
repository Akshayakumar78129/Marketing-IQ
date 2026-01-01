"""
Creative & Messaging - Ad Set Performance repository - Data access layer.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class AdSetPerformanceRepository:
    """Repository for ad set performance data access operations."""

    @staticmethod
    def get_ad_set_performance(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[dict]:
        """
        Fetch ad set performance data for table.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            List of dictionaries with ad set performance metrics
        """
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("date_day >= %(date_from)s::DATE")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("date_day <= %(date_to)s::DATE")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                ad_set_name AS AD_SET,
                campaign_name AS CAMPAIGN,
                SUM(impressions) AS IMPRESSIONS,
                SUM(reach) AS REACH,
                SUM(clicks) AS CLICKS,
                AVG(ctr) AS CTR,
                AVG(cpc) AS CPC,
                SUM(spend) AS SPEND
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_SET_PERFORMANCE
            WHERE platform = 'meta'
            {date_filter}
            GROUP BY ad_set_name, campaign_name
            ORDER BY IMPRESSIONS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ad_set_performance_repository = AdSetPerformanceRepository()
