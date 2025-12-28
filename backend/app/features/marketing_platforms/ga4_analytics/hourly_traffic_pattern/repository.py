"""
GA4 Analytics Hourly Traffic Pattern repository - Data access layer for hourly traffic metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4HourlyTrafficPatternRepository:
    """Repository for GA4 Analytics hourly traffic pattern data access operations."""

    @staticmethod
    def get_hourly_traffic(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch hourly traffic pattern with impressions and clicks.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with hourly traffic metrics
        """
        # Build date filter conditions
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        # Build the date filter clause
        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                h.HOUR_LABEL_12H AS HOUR_LABEL,
                f.HOUR AS HOUR,
                SUM(f.IMPRESSIONS) AS IMPRESSIONS,
                SUM(f.CLICKS) AS CLICKS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_HOURLY f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_HOUR h ON f.HOUR = h.HOUR_OF_DAY
            WHERE f.PLATFORM = 'google_ads'
                {date_filter}
            GROUP BY f.HOUR, h.HOUR_LABEL_12H
            ORDER BY f.HOUR ASC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
ga4_hourly_traffic_pattern_repository = GA4HourlyTrafficPatternRepository()
