"""
Traffic by Source repository - Data access layer for traffic source metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class TrafficBySourceRepository:
    """Repository for traffic by source data access operations."""

    @staticmethod
    def get_traffic_by_source(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch session distribution by source/medium.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with source_medium and sessions
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
                SUM(TOTAL_SESSIONS) AS SESSIONS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_SESSIONS
            {date_filter}
            GROUP BY SOURCE_MEDIUM
            ORDER BY SESSIONS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
traffic_by_source_repository = TrafficBySourceRepository()
