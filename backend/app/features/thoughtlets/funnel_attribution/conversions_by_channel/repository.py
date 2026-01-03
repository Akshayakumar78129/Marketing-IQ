"""
Conversions by Channel repository - Data access layer for channel conversion metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class ConversionsByChannelRepository:
    """Repository for conversions by channel data access operations."""

    @staticmethod
    def get_conversions_by_channel(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[dict]:
        """
        Fetch conversions grouped by marketing channel.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with channel, conversions, and revenue
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
                CHANNEL_GROUPING AS CHANNEL,
                ROUND(SUM(CONVERSIONS)) AS CONVERSIONS,
                ROUND(SUM(REVENUE), 2) AS REVENUE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_FIRST_TOUCH
            {date_filter}
            GROUP BY CHANNEL_GROUPING
            ORDER BY CONVERSIONS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
conversions_by_channel_repository = ConversionsByChannelRepository()
