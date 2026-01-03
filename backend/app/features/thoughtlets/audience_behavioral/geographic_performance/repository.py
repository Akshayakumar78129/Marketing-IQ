"""
Geographic Performance repository - Data access layer for geo performance metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GeographicPerformanceRepository:
    """Repository for geographic performance data access operations."""

    @staticmethod
    def get_geographic_performance(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch geographic performance metrics by country.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with country performance metrics
        """
        date_conditions = ["GEO_LEVEL = 'country'"]
        params = {}

        if date_from:
            date_conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        date_filter = "WHERE " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                LOCATION_VALUE AS COUNTRY,
                SUM(USERS) AS USERS,
                SUM(NEW_USERS) AS NEW_USERS,
                ROUND(SUM(NEW_USERS) * 100.0 / NULLIF(SUM(USERS), 0), 1) AS NEW_USER_PCT,
                SUM(ENGAGED_SESSIONS) AS ENGAGED,
                ROUND(AVG(ENGAGEMENT_RATE) * 100, 1) AS ENG_RATE_PCT
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_GEO
            {date_filter}
            GROUP BY LOCATION_VALUE
            ORDER BY USERS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
geographic_performance_repository = GeographicPerformanceRepository()
