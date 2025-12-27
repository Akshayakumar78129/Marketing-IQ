"""
GA4 Analytics Technology Breakdown repository - Data access layer for technology metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4TechnologyBreakdownRepository:
    """Repository for GA4 Analytics technology breakdown data access operations."""

    @staticmethod
    def get_traffic_sources(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch traffic sources breakdown.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with traffic source metrics
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
                SOURCE,
                SUM(SESSIONS) AS SESSIONS,
                SUM(SESSIONS) * 100.0 / SUM(SUM(SESSIONS)) OVER() AS PERCENTAGE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_TRAFFIC
            WHERE PLATFORM = 'ga4'
                {date_filter}
            GROUP BY SOURCE
            ORDER BY SESSIONS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []

    @staticmethod
    def get_devices(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch devices breakdown.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with device metrics
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
                COALESCE(DEVICE_CATEGORY, 'unknown') AS DEVICE_CATEGORY,
                SUM(USERS) AS USERS,
                SUM(USERS) * 100.0 / SUM(SUM(USERS)) OVER() AS PERCENTAGE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_DEVICE_BROWSER
            WHERE SOURCE_PLATFORM = 'ga4'
                {date_filter}
            GROUP BY DEVICE_CATEGORY
            ORDER BY USERS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []

    @staticmethod
    def get_browsers(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch browsers breakdown.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with browser metrics
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
                BROWSER_GROUP AS BROWSER,
                SUM(USERS) AS USERS,
                SUM(USERS) * 100.0 / SUM(SUM(USERS)) OVER() AS PERCENTAGE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_DEVICE_BROWSER
            WHERE SOURCE_PLATFORM = 'ga4'
                {date_filter}
            GROUP BY BROWSER_GROUP
            ORDER BY USERS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ga4_technology_breakdown_repository = GA4TechnologyBreakdownRepository()
