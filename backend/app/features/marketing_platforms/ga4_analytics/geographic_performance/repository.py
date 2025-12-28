"""
GA4 Analytics Geographic Performance repository - Data access layer for geographic metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4GeographicPerformanceRepository:
    """Repository for GA4 Analytics geographic performance data access operations."""

    @staticmethod
    def get_geographic_performance(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch geographic performance by country.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with geographic performance metrics
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
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                LOCATION_VALUE AS COUNTRY,
                SUM(ENGAGED_SESSIONS) AS SESSIONS,
                SUM(CONVERSIONS) * 100.0 / NULLIF(SUM(USERS), 0) AS CONV_RATE,
                SUM(REVENUE) AS REVENUE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_GEO
            WHERE SOURCE_PLATFORM = 'ga4'
                AND GEO_LEVEL = 'country'
                {date_filter}
            GROUP BY LOCATION_VALUE
            ORDER BY SESSIONS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ga4_geographic_performance_repository = GA4GeographicPerformanceRepository()
