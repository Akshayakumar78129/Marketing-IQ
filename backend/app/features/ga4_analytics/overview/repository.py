"""
GA4 Analytics Overview repository - Data access layer for overview metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4OverviewRepository:
    """Repository for GA4 Analytics overview data access operations."""

    @staticmethod
    def get_overview_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Optional[dict]:
        """
        Fetch aggregated GA4 Analytics overview metrics, optionally filtered by date range.

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

        # Build the date filter clause
        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                SUM(SESSIONS) AS SESSIONS,
                SUM(TOTAL_USERS) AS USERS,
                SUM(ENGAGED_SESSIONS) AS ENGAGED_SESSIONS,
                ROUND(AVG(ENGAGEMENT_RATE) * 100, 1) AS ENGAGEMENT_RATE,
                ROUND(AVG(SESSIONS_PER_USER), 2) AS SESSIONS_PER_USER,
                SUM(CONVERSIONS) AS CONVERSIONS,
                SUM(REVENUE) AS REVENUE,
                ROUND(SUM(REVENUE) / NULLIF(SUM(CONVERSIONS), 0), 2) AS CONVERSION_VALUE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_TRAFFIC
            WHERE PLATFORM = 'ga4'
                {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else None


# Singleton instance for dependency injection
ga4_overview_repository = GA4OverviewRepository()
