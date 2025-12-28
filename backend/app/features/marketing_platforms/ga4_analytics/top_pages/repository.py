"""
GA4 Analytics Top Pages repository - Data access layer for page metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4TopPagesRepository:
    """Repository for GA4 Analytics top pages data access operations."""

    @staticmethod
    def get_top_pages(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch top pages by page views.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with page metrics
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
                SUM(PAGE_VIEWS) AS PAGE_VIEWS,
                SUM(USERS) AS UNIQUE_VIEWS,
                ROUND(SUM(ENGAGEMENT_DURATION_SECONDS) / NULLIF(SUM(USERS), 0), 2) AS AVG_TIME_SECONDS,
                0 AS BOUNCE_RATE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_PAGES
            WHERE PLATFORM = 'ga4'
                {date_filter}
            GROUP BY PAGE_PATH
            ORDER BY PAGE_VIEWS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ga4_top_pages_repository = GA4TopPagesRepository()
