"""
Traffic Source Attribution repository - Data access layer for traffic source attribution metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class TrafficSourceAttributionRepository:
    """Repository for traffic source attribution data access operations."""

    @staticmethod
    def get_traffic_source_attribution(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[dict]:
        """
        Fetch traffic source attribution data grouped by source/medium.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with traffic source attribution data
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
                SOURCE_MEDIUM,
                SUM(SESSIONS) AS SESSIONS,
                SUM(ENGAGED_SESSIONS) AS ENGAGED,
                SUM(TOTAL_USERS) AS USERS,
                ROUND(AVG(ENGAGEMENT_RATE) * 100, 1) AS ENG_RATE_PCT,
                ROUND(SUM(SESSIONS) * 1.0 / NULLIF(SUM(TOTAL_USERS), 0), 1) AS SESS_PER_USER
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_TRAFFIC
            {date_filter}
            GROUP BY SOURCE_MEDIUM
            ORDER BY SESSIONS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
traffic_source_attribution_repository = TrafficSourceAttributionRepository()
