"""
Thoughtlets Core Performance ROAS by Platform repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class RoasByPlatformRepository:
    """Repository for ROAS by platform data access operations."""

    @staticmethod
    def get_roas_by_platform(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch ROAS grouped by platform.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with platform ROAS data
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
                CASE
                    WHEN PLATFORM = 'google_ads' THEN 'Google Ads'
                    WHEN PLATFORM = 'meta' THEN 'Meta Ads'
                    ELSE PLATFORM
                END AS PLATFORM,
                SUM(CONVERSION_VALUE) / NULLIF(SUM(SPEND), 0) AS ROAS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            {date_filter}
            GROUP BY PLATFORM
            ORDER BY ROAS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
roas_by_platform_repository = RoasByPlatformRepository()
