"""
GA4 Analytics Traffic Sources repository - Data access layer for traffic sources.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4TrafficSourcesRepository:
    """Repository for GA4 Analytics traffic sources data access operations."""

    @staticmethod
    def get_traffic_sources(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch traffic sources with sessions, users, and revenue metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with traffic source metrics
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
                SOURCE,
                SUM(SESSIONS) AS SESSIONS,
                SUM(TOTAL_USERS) AS USERS,
                SUM(REVENUE) AS REVENUE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_TRAFFIC
            WHERE PLATFORM = 'ga4'
                {date_filter}
            GROUP BY SOURCE
            ORDER BY SESSIONS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ga4_traffic_sources_repository = GA4TrafficSourcesRepository()
