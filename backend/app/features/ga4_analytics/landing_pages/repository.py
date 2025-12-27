"""
GA4 Analytics Landing Pages repository - Data access layer for landing page metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4LandingPagesRepository:
    """Repository for GA4 Analytics landing pages data access operations."""

    @staticmethod
    def get_landing_pages(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch landing pages by entrances.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with landing page metrics
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
                PAGE_PATH AS PAGE,
                SUM(USERS) AS ENTRANCES,
                0 AS BOUNCE_RATE,
                SUM(USERS) AS SESSIONS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_PAGES
            WHERE PLATFORM = 'ga4'
                {date_filter}
            GROUP BY PAGE_PATH
            ORDER BY ENTRANCES DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ga4_landing_pages_repository = GA4LandingPagesRepository()
