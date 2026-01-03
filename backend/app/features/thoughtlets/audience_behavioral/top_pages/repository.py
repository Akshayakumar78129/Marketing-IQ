"""
Top Pages repository - Data access layer for page metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class TopPagesRepository:
    """Repository for top pages data access operations."""

    @staticmethod
    def get_top_pages(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch top pages with engagement metrics.

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
            date_filter = "WHERE " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                PAGE_PATH,
                PAGE_TYPE,
                SUM(PAGE_VIEWS) AS VIEWS,
                SUM(USERS) AS USERS,
                ROUND(AVG(AVG_ENGAGEMENT_PER_USER), 0) AS AVG_TIME_SECONDS,
                ROUND(SUM(PAGE_VIEWS) / NULLIF(SUM(USERS), 0), 1) AS VIEWS_PER_USER
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_PAGES
            {date_filter}
            GROUP BY PAGE_PATH, PAGE_TYPE
            ORDER BY VIEWS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
top_pages_repository = TopPagesRepository()
