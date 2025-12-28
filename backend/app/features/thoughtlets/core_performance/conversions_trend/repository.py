"""
Thoughtlets Core Performance Conversions Trend repository - Data access layer for monthly conversions.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class ConversionsTrendRepository:
    """Repository for conversions trend data access operations."""

    @staticmethod
    def get_conversions_trend(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch monthly conversions trend across all platforms.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with monthly conversion data
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
                TO_CHAR(DATE_TRUNC('MONTH', DATE_DAY), 'Mon YYYY') AS MONTH,
                SUM(CONVERSIONS) AS CONVERSIONS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            {date_filter}
            GROUP BY DATE_TRUNC('MONTH', DATE_DAY)
            ORDER BY DATE_TRUNC('MONTH', DATE_DAY)
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
conversions_trend_repository = ConversionsTrendRepository()
