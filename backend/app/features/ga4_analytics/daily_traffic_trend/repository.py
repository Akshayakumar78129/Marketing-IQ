"""
GA4 Analytics Daily Traffic Trend repository - Data access layer for daily traffic metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4DailyTrafficTrendRepository:
    """Repository for GA4 Analytics daily traffic trend data access operations."""

    @staticmethod
    def get_daily_traffic(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch daily traffic trend with sessions and users.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with daily traffic metrics
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

        # Build the date filter clause
        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                TO_CHAR(DATE_DAY, 'YYYY-MM-DD') AS DATE,
                SUM(TOTAL_SESSIONS) AS SESSIONS,
                SUM(TOTAL_USERS) AS USERS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_SESSIONS
            WHERE PLATFORM = 'ga4'
                {date_filter}
            GROUP BY DATE_DAY
            ORDER BY DATE_DAY ASC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ga4_daily_traffic_trend_repository = GA4DailyTrafficTrendRepository()
