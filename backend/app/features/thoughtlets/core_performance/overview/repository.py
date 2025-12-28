"""
Thoughtlets Core Performance Overview repository - Data access layer for aggregated metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class CorePerformanceOverviewRepository:
    """Repository for core performance overview data access operations across all platforms."""

    @staticmethod
    def get_overview(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch aggregated core performance metrics across all platforms.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated performance metrics
        """
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
            date_filter = "WHERE " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                SUM(CONVERSIONS) AS CONVERSIONS,
                SUM(CONVERSIONS) * 100.0 / NULLIF(SUM(CLICKS), 0) AS CONVERSION_RATE,
                SUM(SPEND) / NULLIF(SUM(CONVERSIONS), 0) AS COST_PER_CONVERSION,
                SUM(CONVERSION_VALUE) AS REVENUE,
                SUM(CONVERSION_VALUE) / NULLIF(SUM(SPEND), 0) AS ROAS,
                SUM(CLICKS) * 100.0 / NULLIF(SUM(IMPRESSIONS), 0) AS CTR,
                SUM(SPEND) / NULLIF(SUM(CLICKS), 0) AS CPC,
                SUM(IMPRESSIONS) AS IMPRESSIONS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
core_performance_overview_repository = CorePerformanceOverviewRepository()
