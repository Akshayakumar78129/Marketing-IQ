"""
Google Ads Daily Performance Trend repository - Data access layer for daily performance metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class DailyPerformanceTrendRepository:
    """Repository for Google Ads daily performance trend data access operations."""

    @staticmethod
    def get_daily_performance_trend(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch Google Ads daily performance trend by day of week with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with daily performance metrics by day of week
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
                CASE DAYOFWEEK(DATE_DAY)
                    WHEN 0 THEN 'Sunday'
                    WHEN 1 THEN 'Monday'
                    WHEN 2 THEN 'Tuesday'
                    WHEN 3 THEN 'Wednesday'
                    WHEN 4 THEN 'Thursday'
                    WHEN 5 THEN 'Friday'
                    WHEN 6 THEN 'Saturday'
                END AS "DAY_NAME",
                CASE DAYOFWEEK(DATE_DAY)
                    WHEN 0 THEN 7
                    ELSE DAYOFWEEK(DATE_DAY)
                END AS "DAY_ORDER",
                SUM(CONVERSIONS) AS "TOTAL_CONVERSIONS",
                SUM(SPEND) AS "TOTAL_SPEND"
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            WHERE PLATFORM = 'google_ads'
                {filter_clause}
            GROUP BY DAYOFWEEK(DATE_DAY)
            ORDER BY "DAY_ORDER"
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
daily_performance_trend_repository = DailyPerformanceTrendRepository()
