"""
Thoughtlets Spend and Budget - Spend by Platform repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class SpendByPlatformRepository:
    """Repository for spend by platform data access operations."""

    @staticmethod
    def get_spend_by_platform(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch spend breakdown by platform.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with platform and spend data
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
                PLATFORM,
                SUM(SPEND) AS SPEND
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            {date_filter}
            GROUP BY PLATFORM
            ORDER BY SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
spend_by_platform_repository = SpendByPlatformRepository()
